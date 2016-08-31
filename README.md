# Import-iOS-Localizable.strings-to-Android-strings.xml
将iOS与Android的项目中相同的中文字符串资源倒入到Android项目中。

###背景
* 需要做语言国际化，但是只对iOS的语言资源做了翻译.....
* iOS语言中文资源文件中，key与value相同

###用法
* 配置android_paths和ios_paths
* 运行

###坑
* 对通配符只对iOS中的%@做了%(n)@s处理，没有考虑语法顺序
* 待补充
