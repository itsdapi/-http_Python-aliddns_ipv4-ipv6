# Docker实现阿里云域名DDNS支持ipv4和ipv6
> 使用url请求来将新的公网地址同步到阿里云

## Best Practice
搭配RouterOS内置的脚本功能可以实现公网地址更新，而且不依赖于任何的第三方公网ip获取工具，有效避免梯子等原因导致无法获取正确ip，或者第三方网站暂时下线等原因

## 食用方法
用写好的Docker-compose就能从源码编译并启动，后续我也会push到docker hub

## 环境变量

| ENV          | desc    |
|--------------|---------|
| ACCESSKEYID  | 阿里云访问id |
| ACCESSSECRET | 阿里云访问密钥 |
| DOMAIN       | 目标域名    |
| NAME_IPV4    | ipv4前缀  |
| NAME_IPV6    | ipv6前缀  |





