class UrlHeaders:

    @classmethod
    def getHeader(self):
        # expires = Thu, 12 - Dec - 2019 10: 31:40 GMT
        return {
            'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML, like Gecko) '
                          'Chrome/52.0.2743.116 Safari/537.36 ',
            'Cookie': 'MB=pc; LB=pc; RecUsr=1910022234279592; _ga=GA1.3.1126261753.1570023268; AC=1; '
                      'UID=1910022238386214wn7hxx880jtzz0rfkjswe6bqunrl; wkbsn=azVyKwBM41wF5IB0jwMq; '
                      'apay-session-set=true; AdultsFlg=True; ASP.NET_SessionId=drax5q20yd3d3lrvsp33atd0; MyIcon=0; '
                      '_gid=GA1.3.1487069046.1570956640; Top=101; _gat=1; '
                      'CheckHistory=10576022%2C10647856%2C10602777%2C10637749%2C10645838%2C10641521%2C10575031',
        }
