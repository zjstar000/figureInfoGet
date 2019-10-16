class UrlHeaders:

    @classmethod
    def getHeader(self):
        # expires = Thu, 12 - Dec - 2019 10: 31:40 GMT
        return {
            'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML, like Gecko) '
                          'Chrome/52.0.2743.116 Safari/537.36 ',
            'Cookie': 'MB=pc; LB=pc; RecUsr=1910022234279592; _ga=GA1.3.1126261753.1570023268; AC=1; '
                      'apay-session-set=true; AdultsFlg=True; _gid=GA1.3.1487069046.1570956640; Top=101; '
                      'ASP.NET_SessionId=kxgnfe4narhxo1vnysg1s1u1; wkbsn=uenzRnjDeYF0hxeWIG5a; '
                      'UID=191016205743909469cu1qr8dpqafzpfg0yr4b1sumvy; MyIcon=0; '
                      'CheckHistory=10648739%2C10646109%2C10648833%2C10646338%2C%2C%2C; _gat=1',
        }
