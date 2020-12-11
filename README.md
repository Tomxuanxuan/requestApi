# requestApi
接口请求（参数：用MD5加密的字符串）
APP密钥：APP_key
刷新密钥：refresh_key
请求密钥：request_key

a. 当请求秘钥失效后，请使用APP_KEY、刷新秘钥获取刷新秘钥和请求秘钥；
b. 当刷新秘钥失效后，请使用APP_KEY、APP秘钥获取刷新秘钥与请求秘钥。

使用上面两种调用方式后，刷新秘钥和请求秘钥都会重新生成，并生成新的有效期限。
刷新秘钥有效时间为48小时，请求秘钥有效时间为15分钟。

调用获取秘钥接口时，必须输入以下三个参数
appKey：应用的APP_KEY, 
sign：用MD5加密的字符串（字母全部小写）,MD5（APP_KEY+秘钥（APP秘钥/刷新秘钥）+long类型请求时间）；
requestTime：请求时间(long类型的字符串)。
