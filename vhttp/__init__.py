# vttp/__init__.py
# vttp
# Author: Rushy Panchal
# Date: December 29th, 2017
# Description: vHTTP is a SOCKS5-based proxy for HTTP that utilizes multiple
#              vantage-points to validate received data. Requests are
#              replicated to numerous proxies, and the content of the responses
#              are compared. If specified quorum is not achieved among the
#              responses, then an error is returned to the user instead.
