# Generated by Django 3.2.11 on 2022-02-15 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('columns', '0016_auto_20220215_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='aggregationcolumn',
            name='currency',
            field=models.CharField(blank=True, choices=[('AED', 'AED - د.إ'), ('AFN', 'AFN - ؋'), ('ALL', 'ALL - L'), ('AMD', 'AMD - ֏'), ('ANG', 'ANG - ƒ'), ('AOA', 'AOA - Kz'), ('ARS', 'ARS - $'), ('AUD', 'AUD - $'), ('AWG', 'AWG - ƒ'), ('AZN', 'AZN - ₼'), ('BAM', 'BAM - KM'), ('BBD', 'BBD - $'), ('BDT', 'BDT - ৳'), ('BGN', 'BGN - лв'), ('BHD', 'BHD - .د.ب'), ('BIF', 'BIF - FBu'), ('BMD', 'BMD - $'), ('BND', 'BND - $'), ('BOB', 'BOB - $b'), ('BRL', 'BRL - R$'), ('BSD', 'BSD - $'), ('BTC', 'BTC - ฿'), ('BTN', 'BTN - Nu.'), ('BWP', 'BWP - P'), ('BYR', 'BYR - Br'), ('BYN', 'BYN - Br'), ('BZD', 'BZD - BZ$'), ('CAD', 'CAD - $'), ('CDF', 'CDF - FC'), ('CHF', 'CHF - CHF'), ('CLP', 'CLP - $'), ('CNY', 'CNY - ¥'), ('COP', 'COP - $'), ('CRC', 'CRC - ₡'), ('CUC', 'CUC - $'), ('CUP', 'CUP - ₱'), ('CVE', 'CVE - $'), ('CZK', 'CZK - Kč'), ('DJF', 'DJF - Fdj'), ('DKK', 'DKK - kr'), ('DOP', 'DOP - RD$'), ('DZD', 'DZD - دج'), ('EEK', 'EEK - kr'), ('EGP', 'EGP - £'), ('ERN', 'ERN - Nfk'), ('ETB', 'ETB - Br'), ('ETH', 'ETH - Ξ'), ('EUR', 'EUR - €'), ('FJD', 'FJD - $'), ('FKP', 'FKP - £'), ('GBP', 'GBP - £'), ('GEL', 'GEL - ₾'), ('GGP', 'GGP - £'), ('GHC', 'GHC - ₵'), ('GHS', 'GHS - GH₵'), ('GIP', 'GIP - £'), ('GMD', 'GMD - D'), ('GNF', 'GNF - FG'), ('GTQ', 'GTQ - Q'), ('GYD', 'GYD - $'), ('HKD', 'HKD - $'), ('HNL', 'HNL - L'), ('HRK', 'HRK - kn'), ('HTG', 'HTG - G'), ('HUF', 'HUF - Ft'), ('IDR', 'IDR - Rp'), ('ILS', 'ILS - ₪'), ('IMP', 'IMP - £'), ('INR', 'INR - ₹'), ('IQD', 'IQD - ع.د'), ('IRR', 'IRR - ﷼'), ('ISK', 'ISK - kr'), ('JEP', 'JEP - £'), ('JMD', 'JMD - J$'), ('JOD', 'JOD - JD'), ('JPY', 'JPY - ¥'), ('KES', 'KES - KSh'), ('KGS', 'KGS - лв'), ('KHR', 'KHR - ៛'), ('KMF', 'KMF - CF'), ('KPW', 'KPW - ₩'), ('KRW', 'KRW - ₩'), ('KWD', 'KWD - KD'), ('KYD', 'KYD - $'), ('KZT', 'KZT - лв'), ('LAK', 'LAK - ₭'), ('LBP', 'LBP - £'), ('LKR', 'LKR - ₨'), ('LRD', 'LRD - $'), ('LSL', 'LSL - M'), ('LTC', 'LTC - Ł'), ('LTL', 'LTL - Lt'), ('LVL', 'LVL - Ls'), ('LYD', 'LYD - LD'), ('MAD', 'MAD - MAD'), ('MDL', 'MDL - lei'), ('MGA', 'MGA - Ar'), ('MKD', 'MKD - ден'), ('MMK', 'MMK - K'), ('MNT', 'MNT - ₮'), ('MOP', 'MOP - MOP$'), ('MRO', 'MRO - UM'), ('MRU', 'MRU - UM'), ('MUR', 'MUR - ₨'), ('MVR', 'MVR - Rf'), ('MWK', 'MWK - MK'), ('MXN', 'MXN - $'), ('MYR', 'MYR - RM'), ('MZN', 'MZN - MT'), ('NAD', 'NAD - $'), ('NGN', 'NGN - ₦'), ('NIO', 'NIO - C$'), ('NOK', 'NOK - kr'), ('NPR', 'NPR - ₨'), ('NZD', 'NZD - $'), ('OMR', 'OMR - ﷼'), ('PAB', 'PAB - B/.'), ('PEN', 'PEN - S/.'), ('PGK', 'PGK - K'), ('PHP', 'PHP - ₱'), ('PKR', 'PKR - ₨'), ('PLN', 'PLN - zł'), ('PYG', 'PYG - Gs'), ('QAR', 'QAR - ﷼'), ('RMB', 'RMB - ￥'), ('RON', 'RON - lei'), ('RSD', 'RSD - Дин.'), ('RUB', 'RUB - ₽'), ('RWF', 'RWF - R₣'), ('SAR', 'SAR - ﷼'), ('SBD', 'SBD - $'), ('SCR', 'SCR - ₨'), ('SDG', 'SDG - ج.س.'), ('SEK', 'SEK - kr'), ('SGD', 'SGD - $'), ('SHP', 'SHP - £'), ('SLL', 'SLL - Le'), ('SOS', 'SOS - S'), ('SRD', 'SRD - $'), ('SSP', 'SSP - £'), ('STD', 'STD - Db'), ('STN', 'STN - Db'), ('SVC', 'SVC - $'), ('SYP', 'SYP - £'), ('SZL', 'SZL - E'), ('THB', 'THB - ฿'), ('TJS', 'TJS - SM'), ('TMT', 'TMT - T'), ('TND', 'TND - د.ت'), ('TOP', 'TOP - T$'), ('TRL', 'TRL - ₤'), ('TRY', 'TRY - ₺'), ('TTD', 'TTD - TT$'), ('TVD', 'TVD - $'), ('TWD', 'TWD - NT$'), ('TZS', 'TZS - TSh'), ('UAH', 'UAH - ₴'), ('UGX', 'UGX - USh'), ('USD', 'USD - $'), ('UYU', 'UYU - $U'), ('UZS', 'UZS - лв'), ('VEF', 'VEF - Bs'), ('VND', 'VND - ₫'), ('VUV', 'VUV - VT'), ('WST', 'WST - WS$'), ('XAF', 'XAF - FCFA'), ('XBT', 'XBT - Ƀ'), ('XCD', 'XCD - $'), ('XOF', 'XOF - CFA'), ('XPF', 'XPF - ₣'), ('YER', 'YER - ﷼'), ('ZAR', 'ZAR - R'), ('ZWD', 'ZWD - Z$')], help_text='Select a currency', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='aggregationcolumn',
            name='name',
            field=models.CharField(blank=True, help_text='Set column header name', max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='aggregationcolumn',
            name='rounding',
            field=models.IntegerField(blank=True, default=2, help_text='Decimal point to round to'),
        ),
        migrations.AddField(
            model_name='column',
            name='currency',
            field=models.CharField(blank=True, choices=[('AED', 'AED - د.إ'), ('AFN', 'AFN - ؋'), ('ALL', 'ALL - L'), ('AMD', 'AMD - ֏'), ('ANG', 'ANG - ƒ'), ('AOA', 'AOA - Kz'), ('ARS', 'ARS - $'), ('AUD', 'AUD - $'), ('AWG', 'AWG - ƒ'), ('AZN', 'AZN - ₼'), ('BAM', 'BAM - KM'), ('BBD', 'BBD - $'), ('BDT', 'BDT - ৳'), ('BGN', 'BGN - лв'), ('BHD', 'BHD - .د.ب'), ('BIF', 'BIF - FBu'), ('BMD', 'BMD - $'), ('BND', 'BND - $'), ('BOB', 'BOB - $b'), ('BRL', 'BRL - R$'), ('BSD', 'BSD - $'), ('BTC', 'BTC - ฿'), ('BTN', 'BTN - Nu.'), ('BWP', 'BWP - P'), ('BYR', 'BYR - Br'), ('BYN', 'BYN - Br'), ('BZD', 'BZD - BZ$'), ('CAD', 'CAD - $'), ('CDF', 'CDF - FC'), ('CHF', 'CHF - CHF'), ('CLP', 'CLP - $'), ('CNY', 'CNY - ¥'), ('COP', 'COP - $'), ('CRC', 'CRC - ₡'), ('CUC', 'CUC - $'), ('CUP', 'CUP - ₱'), ('CVE', 'CVE - $'), ('CZK', 'CZK - Kč'), ('DJF', 'DJF - Fdj'), ('DKK', 'DKK - kr'), ('DOP', 'DOP - RD$'), ('DZD', 'DZD - دج'), ('EEK', 'EEK - kr'), ('EGP', 'EGP - £'), ('ERN', 'ERN - Nfk'), ('ETB', 'ETB - Br'), ('ETH', 'ETH - Ξ'), ('EUR', 'EUR - €'), ('FJD', 'FJD - $'), ('FKP', 'FKP - £'), ('GBP', 'GBP - £'), ('GEL', 'GEL - ₾'), ('GGP', 'GGP - £'), ('GHC', 'GHC - ₵'), ('GHS', 'GHS - GH₵'), ('GIP', 'GIP - £'), ('GMD', 'GMD - D'), ('GNF', 'GNF - FG'), ('GTQ', 'GTQ - Q'), ('GYD', 'GYD - $'), ('HKD', 'HKD - $'), ('HNL', 'HNL - L'), ('HRK', 'HRK - kn'), ('HTG', 'HTG - G'), ('HUF', 'HUF - Ft'), ('IDR', 'IDR - Rp'), ('ILS', 'ILS - ₪'), ('IMP', 'IMP - £'), ('INR', 'INR - ₹'), ('IQD', 'IQD - ع.د'), ('IRR', 'IRR - ﷼'), ('ISK', 'ISK - kr'), ('JEP', 'JEP - £'), ('JMD', 'JMD - J$'), ('JOD', 'JOD - JD'), ('JPY', 'JPY - ¥'), ('KES', 'KES - KSh'), ('KGS', 'KGS - лв'), ('KHR', 'KHR - ៛'), ('KMF', 'KMF - CF'), ('KPW', 'KPW - ₩'), ('KRW', 'KRW - ₩'), ('KWD', 'KWD - KD'), ('KYD', 'KYD - $'), ('KZT', 'KZT - лв'), ('LAK', 'LAK - ₭'), ('LBP', 'LBP - £'), ('LKR', 'LKR - ₨'), ('LRD', 'LRD - $'), ('LSL', 'LSL - M'), ('LTC', 'LTC - Ł'), ('LTL', 'LTL - Lt'), ('LVL', 'LVL - Ls'), ('LYD', 'LYD - LD'), ('MAD', 'MAD - MAD'), ('MDL', 'MDL - lei'), ('MGA', 'MGA - Ar'), ('MKD', 'MKD - ден'), ('MMK', 'MMK - K'), ('MNT', 'MNT - ₮'), ('MOP', 'MOP - MOP$'), ('MRO', 'MRO - UM'), ('MRU', 'MRU - UM'), ('MUR', 'MUR - ₨'), ('MVR', 'MVR - Rf'), ('MWK', 'MWK - MK'), ('MXN', 'MXN - $'), ('MYR', 'MYR - RM'), ('MZN', 'MZN - MT'), ('NAD', 'NAD - $'), ('NGN', 'NGN - ₦'), ('NIO', 'NIO - C$'), ('NOK', 'NOK - kr'), ('NPR', 'NPR - ₨'), ('NZD', 'NZD - $'), ('OMR', 'OMR - ﷼'), ('PAB', 'PAB - B/.'), ('PEN', 'PEN - S/.'), ('PGK', 'PGK - K'), ('PHP', 'PHP - ₱'), ('PKR', 'PKR - ₨'), ('PLN', 'PLN - zł'), ('PYG', 'PYG - Gs'), ('QAR', 'QAR - ﷼'), ('RMB', 'RMB - ￥'), ('RON', 'RON - lei'), ('RSD', 'RSD - Дин.'), ('RUB', 'RUB - ₽'), ('RWF', 'RWF - R₣'), ('SAR', 'SAR - ﷼'), ('SBD', 'SBD - $'), ('SCR', 'SCR - ₨'), ('SDG', 'SDG - ج.س.'), ('SEK', 'SEK - kr'), ('SGD', 'SGD - $'), ('SHP', 'SHP - £'), ('SLL', 'SLL - Le'), ('SOS', 'SOS - S'), ('SRD', 'SRD - $'), ('SSP', 'SSP - £'), ('STD', 'STD - Db'), ('STN', 'STN - Db'), ('SVC', 'SVC - $'), ('SYP', 'SYP - £'), ('SZL', 'SZL - E'), ('THB', 'THB - ฿'), ('TJS', 'TJS - SM'), ('TMT', 'TMT - T'), ('TND', 'TND - د.ت'), ('TOP', 'TOP - T$'), ('TRL', 'TRL - ₤'), ('TRY', 'TRY - ₺'), ('TTD', 'TTD - TT$'), ('TVD', 'TVD - $'), ('TWD', 'TWD - NT$'), ('TZS', 'TZS - TSh'), ('UAH', 'UAH - ₴'), ('UGX', 'UGX - USh'), ('USD', 'USD - $'), ('UYU', 'UYU - $U'), ('UZS', 'UZS - лв'), ('VEF', 'VEF - Bs'), ('VND', 'VND - ₫'), ('VUV', 'VUV - VT'), ('WST', 'WST - WS$'), ('XAF', 'XAF - FCFA'), ('XBT', 'XBT - Ƀ'), ('XCD', 'XCD - $'), ('XOF', 'XOF - CFA'), ('XPF', 'XPF - ₣'), ('YER', 'YER - ﷼'), ('ZAR', 'ZAR - R'), ('ZWD', 'ZWD - Z$')], help_text='Select a currency', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='column',
            name='name',
            field=models.CharField(blank=True, help_text='Set column header name', max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='column',
            name='rounding',
            field=models.IntegerField(blank=True, default=2, help_text='Decimal point to round to'),
        ),
    ]
