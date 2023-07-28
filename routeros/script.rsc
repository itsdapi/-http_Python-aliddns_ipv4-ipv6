:local pppState
:local publicIP
:set pppState [/interface get [/interface find name="pppoe-out1"] running]

:if ($pppState=true) do={
    :set publicIP [/ip address get [/ip address find dynamic=yes interface="pppoe-out1"] address]
    :set publicIP [:pick $publicIP 0 ([:len $publicIP ] -3)]
    :tool fetch output=none url="http://192.168.0.16:5002/updateV4?ip=$publicIP&domain=catslab.cn&record=*"
    :tool fetch output=none url="http://192.168.0.16:5002/updateV4?ip=$publicIP&domain=catslab.cn&record=@"
}