#!/usr/bin/env python
# encoding: UTF-8
# Refund paypal function
# Author: Guillermo Siliceo Trueba #

from paypal_driver.driver import PayPal
from paypal_api.interface import PayPalInterface
from paypal_api.settings import PayPalConfig

def clean(line):
    line = str(line)
    return line.replace('[','').replace(']','').replace("'",'')

PAYPAL_USER = ''
PAYPAL_PASSWORD = ''
PAYPAL_SIGNATURE = ''
payments_transaction = [] #a list of paypal transaction ids
currency = 'MXN' # the currency the refunded user will get

config = PayPalConfig(API_ENVIRONMENT='production',
                      API_USERNAME=PAYPAL_USER,
                      API_PASSWORD=PAYPAL_PASSWORD,
                      API_SIGNATURE=PAYPAL_SIGNATURE,
                      )
paypalchecker = PayPalInterface(config)
def refund_concert(payments_):
    #lets handle paypal payments first
    for invoice in payments_transaction:
        print '---------------------------------------------'
        print 'For the transaction with invoice number %s'%invoice
        paypal_response = paypalchecker.get_transaction_details(invoice)
        data = paypal_response.raw
        if paypal_response.success:
            # now get the total of the items
            i = 0
            paypaltotal = 0
            while True:
                current = 'AMT_%s'%i
                if i == 0:
                    current = 'AMT'
                i += 1
                if current in paypal_response.raw:
                    paypaltotal += int(float(clean(data[current])))
                else:
                    break
            print 'Paypal reported the transaction by %s is %s with a total cost of \
                    %s'%(clean(data['FIRSTNAME']),
                         clean(data['LASTNAME']),
                         clean(data['PAYMENTSTATUS']),
                         paypaltotal)
            moving_on = str(raw_input('¿Do you want to refund this payment y/n '))
            if moving_on == 'n':
                continue
            elif moving_on == 'y':
                paypal_driver = PayPal()
                paypal_driver.RefundTransaction(transid = invoice, 
                    refundtype = 'Full',
                    currency = currency, 
                    )
                print 'Paypal reporte this transaction as',paypal_driver.api_response['ACK']
        else:
            print 'no response from paypal api for transaction %s probably it \
                 doesnt exist',invoice
