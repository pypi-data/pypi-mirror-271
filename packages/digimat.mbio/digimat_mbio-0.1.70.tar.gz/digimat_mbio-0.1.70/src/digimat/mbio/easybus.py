#!/bin/python

from __future__ import annotations


from .xmlconfig import XMLConfig
from .gateway import MBIOGateway
from .device import MBIODevice


class MBIOGatewayEasybus(MBIOGateway):
    def onInit(self):
        self.GROUP={}

    def loadDevices(self, xml: XMLConfig):
        try:
            bus=xml.children('bus')
            if bus:
                for b in bus:
                    if not b.getBool('enable', True):
                        continue

                    address=b.getInt('address')
                    try:
                        if self.device(address):
                            self.logger.error('Duplicate DEVICE declaration GW%s[%d]' % (self.key, address))
                            continue

                        MBIODeviceEasybusMaster(self, address, xml=b)
                    except:
                        self.logger.error('Error declaring DEVICE GW:%s (%s)' % (self.key, b.tostring()))
        except:
            self.logger.exception('loadDevices(GW:%s)' % self.key)

    def declareDeviceFromName(self, vendor, model, address, xml: XMLConfig = None):
        raise NotImplementedError('declareDeviceFromName')

    def probe(self, address):
        try:
            self.logger.debug('Probing device address %d' % address)
            self.checkIdleAfterSend()
            r=self._client.read_input_registers(0, 10, slave=address)
            self.signalMessageTransmission()
            if r and not r.isError():
                regs=r.registers
                if regs[5]>0:
                    data={'address': address,
                        'vendor': 'Easybus3',
                        'model': 'Easy-M',
                        'version': str(regs[5])}
                    self.logger.info('Found device [%s] [%s] %s at address %d' %
                                    (data['vendor'], data['model'], data['version'], address))
                    return data
        except:
            pass

    def group(self, ccf):
        try:
            group=ccf['group']
            if group:
                return self.GROUP[group.lower()]
        except:
            pass

    def addToGroup(self, group, ccf):
        if group and ccf:
            if not self.group(ccf):
                group=group.lower()
                data={'ccf': [],
                      'open': False, 'closed': False, 'smoke': False, 'error': False, 'cmd': None,
                      'values': {}}
                data['values']['open']=self.valueDigital('ccf%s_open' % group)
                data['values']['closed']=self.valueDigital('ccf%s_closed' % group)
                data['values']['error']=self.valueDigital('ccf%s_err' % group)
                data['values']['smoke']=self.valueDigital('ccf%s_smoke' % group)
                data['values']['cmd']=self.valueDigital('ccf%s_cmd' % group, writable=True)
                self.GROUP[group]=data
            self.GROUP[group]['ccf'].append(ccf)

    def groupRefresh(self):
        if self.GROUP:
            for group in self.GROUP.values():
                if group['ccf']:
                    group['open']=True
                    group['closed']=True
                    group['smoke']=False
                    group['error']=False
                    for ccf in group['ccf']:
                        if ccf['open'] is not True:
                            group['open']=False
                        if ccf['closed'] is not True:
                            group['closed']=False
                        if ccf['smoke']:
                            group['smoke']=True
                        if ccf['error']:
                            group['error']=True

                    error=group['error']
                    group['values']['open'].updateValue(group['open'])
                    group['values']['open'].setError(error)
                    group['values']['closed'].updateValue(group['closed'])
                    group['values']['closed'].setError(error)
                    group['values']['smoke'].updateValue(group['smoke'])
                    group['values']['smoke'].setError(error)
                    group['values']['error'].updateValue(error)

    def configurator(self):
        return None

    def signalSync(self, delay=0):
        for device in self.devices:
            device.sync()


class MBIODeviceEasybusMaster(MBIODevice):
    def buildKey(self, gateway, address):
        return '%s_b%d' % (gateway.key, address)

    def probe(self):
        self.logger.debug('Probing device address %d' % self.address)
        r=self.readInputRegisters(0, 10)
        if r and r[5]>0:
            data={'version': str(r[5]),
                  'vendor': 'Easybus3',
                  'model': 'Easy-M'}
            return data

    def load(self, xml: XMLConfig):
        if xml:
            try:
                self.onLoad(xml)
            except:
                self.logger.exception('%s:%s:load()' % (self.__class__.__name__, self.key))

    def ccf(self, address):
        try:
            return self.CCF[int(address)]
        except:
            pass

    def onInit(self):
        self.valueDigital('run')
        self.valueDigital('fire')
        self.value('slaves', unit=0xff)
        self.value('slaveserr', unit=0xff)
        self.value('cycle', unit='ms')
        self.CCF={}
        self.setPingRegister(0, True)

    def onLoad(self, xml: XMLConfig):
        for ccf in xml.children('ccf'):
            if not ccf.getBool('enable', True):
                continue
            address=ccf.getInt('address')
            group=ccf.get('group')
            if address is not None:
                data={'type': 'ccf', 'address': address, 'group': None,
                      'open': False, 'closed': False, 'error': False, 'smoke': False, 'cmd': None,
                      'info': None, 'state': 0,
                      'values': {'cmd': None}}
                data['values']['open']=self.valueDigital('ccf%d_open' % address)
                data['values']['closed']=self.valueDigital('ccf%d_closed' % address)
                data['values']['error']=self.valueDigital('ccf%d_err' % address)
                data['values']['smoke']=self.valueDigital('ccf%d_smoke' % address)
                if group:
                    data['group']=group
                    self.gateway.addToGroup(group, data)
                else:
                    data['values']['cmd']=self.valueDigital('ccf%d_cmd' % address, writable=True)

                self.CCF[address]=data

    def poweron(self):
        return True

    def poweroff(self):
        return True

    def refresh(self):
        r=self.readInputRegisters(0, 10)
        if r:
            self.values.slaves.updateValue(r[1])
            self.values.slaveserr.updateValue(r[2])
            self.values.fire.updateValue(r[0]==3)
            self.values.run.updateValue(r[0]==1)
            self.values.cycle.updateValue(r[4])

        # Reset to RUN
        r=self.readHoldingRegisters(0, 1)
        if r and r[0]==3:
            self.writeHoldingRegisters(0, 1)

        r=self.readInputRegisters(10, 64)
        if r:
            for ccf in self.CCF.values():
                address=ccf['address']
                n=((address-1) // 2)
                sh=(address-1) % 2
                v=((r[n]) >> (8*sh)) & 0xff
                ccf['info']=v

        r=self.readInputRegisters(300, 32)
        if r:
            for ccf in self.CCF.values():
                address=ccf['address']
                n=((address-1) // 4)
                sh=(address-1) % 4
                v=((r[n]) >> (4*sh)) & 0xf

                # bits 3210:FOCE (F=Fire, O=Open, C=Closed, E=Error)
                ccf['state']=v

                ccf['open']=False
                ccf['closed']=False
                ccf['error']=False
                ccf['smoke']=False

                if v & 0x1:
                    ccf['error']=True
                if v & 0x2:
                    ccf['closed']=True
                if v & 0x4:
                    ccf['open']=True
                if v & 0x8:
                    ccf['smoke']=True

                if ccf['info'] is not None:
                    if ccf['info'] not in [5, 6] or ccf['info'] & 0x80:
                        ccf['error']=True

                # Update values
                error=ccf['error']
                ccf['values']['error'].updateValue(error)
                ccf['values']['open'].updateValue(ccf['open'])
                ccf['values']['open'].setError(error)
                ccf['values']['closed'].updateValue(ccf['closed'])
                ccf['values']['closed'].setError(error)
                ccf['values']['smoke'].updateValue(ccf['smoke'])
                ccf['values']['smoke'].setError(error)
                if ccf['values']['cmd'] is not None:
                    ccf['values']['cmd'].setError(error)
            else:
                ccf['values']['error'].updateValue(True)
                for value in ccf['values'].values():
                    if value is not None:
                        value.setError(True)

            self.gateway.groupRefresh()

        return 3.0

    def sync(self):
        # read actual cmd registers
        r=self.readHoldingRegisters(300, 8)
        if r:
            for ccf in self.CCF.values():
                address=ccf['address']
                n=((address-1) // 16)
                sh=(address-1) % 16

                cmd=ccf['values']['cmd']
                group=self.gateway.group(ccf)
                if group:
                    cmd=group['values']['cmd']

                if cmd.toReachValue is not None:
                    if cmd.toReachValue:
                        r[n] |= (1 << sh)
                    else:
                        r[n] = (r[n] & (~(1 << sh) & 0xffff))

            # update cmd registers
            if self.writeHoldingRegisters(300, r):
                for ccf in self.CCF.values():
                    if ccf['values']['cmd'] is not None:
                        ccf['values']['cmd'].clearSyncAndUpdateValue()
                for group in self.gateway.GROUP.values():
                    group['values']['cmd'].clearSyncAndUpdateValue()


if __name__ == "__main__":
    pass
