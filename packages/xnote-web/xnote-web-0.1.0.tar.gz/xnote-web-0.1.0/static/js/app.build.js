// @author xupingmao
// @since 2017/08/16
// @modified 2021/08/15 12:19:12

////////////////////////////////////////////////////////////////////////////
/**
 * Array 兼容增强包
 */
// 4.1 作为函数调用 Array 构造器
// 4.1.1 Array ( [ item1 [ , item2 [ , … ] ] ] )
// 4.2 Array 构造器
// 4.2.1 new Array ( [ item0 [ , item1 [ , … ] ] ] )
// 4.2.2 new Array (len)
// 4.3 Array 构造器的属性
// 4.3.1 Array.prototype
// 4.3.2 Array.isArray ( arg )
// 4.4 数组原型对象的属性
// 4.4.1 Array.prototype.constructor
// 4.4.2 Array.prototype.toString ( )
// 4.4.3 Array.prototype.toLocaleString ( )
// 4.4.4 Array.prototype.concat ( [ item1 [ , item2 [ , … ] ] ] )
// 4.4.5 Array.prototype.join (separator)
// 4.4.6 Array.prototype.pop ( )
// 4.4.7 Array.prototype.push ( [ item1 [ , item2 [ , … ] ] ] )
// 4.4.8 Array.prototype.reverse ( )
// 4.4.9 Array.prototype.shift ( )
// 4.4.10 Array.prototype.slice (start, end)
// 4.4.11 Array.prototype.sort (comparefn)
// 4.4.12 Array.prototype.splice (start, deleteCount [ , item1 [ , item2 [ , … ] ] ] )
//        arr.splice(2,0,item) ==> arr.insert(2, item)
// 4.4.13 Array.prototype.unshift ( [ item1 [ , item2 [ , … ] ] ] )
// 4.4.14 Array.prototype.indexOf ( searchElement [ , fromIndex ] )
// 4.4.15 Array.prototype.lastIndexOf ( searchElement [ , fromIndex ] )
// 4.4.16 Array.prototype.every ( callbackfn [ , thisArg ] )
// 4.4.17 Array.prototype.some ( callbackfn [ , thisArg ] )
// 4.4.18 Array.prototype.forEach ( callbackfn [ , thisArg ] )
// 4.4.19 Array.prototype.map ( callbackfn [ , thisArg ] )
// 4.4.20 Array.prototype.filter ( callbackfn [ , thisArg ] )
// 4.4.21 Array.prototype.reduce ( callbackfn [ , initialValue ] )
// 4.4.22 Array.prototype.reduceRight ( callbackfn [ , initialValue ] )
// 4.5 Array 实例的属性
// 4.5.1 [[DefineOwnProperty]] ( P, Desc, Throw )
// 4.5.2 length

/**
 * 判断数组中是否存在以start开头的字符串
 * @param {string} start
 */
Array.prototype.startsWith = Array.prototype.startsWith || function (start) {
    var array = this;
    for (var key in array) {
        var item = array[key];
        if (item === start) return true;
    }
    return false;
}

// Array.prototype.each = Array.prototype.each || function (callback) {
//     var self = this;
//     for (var i = 0; i < self.length; i++) {
//         var item = self[i];
//         callback(i, item);
//     }
// }

/**
 * forEach遍历
 * @param {function} callback
 */
Array.prototype.forEach = Array.prototype.forEach || function (callback) {
    var self = this;
    for (var i = 0; i < self.length; i++) {
        var item = self[i];
        callback(item, i, self);
    }
}


/**
 * filter 函数兼容
 */
if (!Array.prototype.filter) {
  Array.prototype.filter = function(fun) {
    if (this === void 0 || this === null) {
      throw new TypeError();
    }

    var t = Object(this);
    var len = t.length >>> 0;
    if (typeof fun !== "function") {
      throw new TypeError();
    }

    var res = [];
    var thisArg = arguments.length >= 2 ? arguments[1] : void 0;
    for (var i = 0; i < len; i++) {
      if (i in t) {
        var val = t[i];
        // NOTE: Technically this should Object.defineProperty at
        //       the next index, as push can be affected by
        //       properties on Object.prototype and Array.prototype.
        //       But that method's new, and collisions should be
        //       rare, so use the more-compatible alternative.
        if (fun.call(thisArg, val, i, t))
          res.push(val);
      }
    }

    return res;
  };
}


// 遍历对象
function objForEach(obj, fn) {
    var key = void 0,
        result = void 0;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) {
            result = fn.call(obj, key, obj[key]);
            if (result === false) {
                break;
            }
        }
    }
};

// 遍历类数组
function arrForEach(fakeArr, fn) {
    var i = void 0,
        item = void 0,
        result = void 0;
    var length = fakeArr.length || 0;
    for (i = 0; i < length; i++) {
        item = fakeArr[i];
        result = fn.call(fakeArr, item, i);
        if (result === false) {
            break;
        }
    }
};

// @author xupingmao
// @since 2017/08/16
// @modified 2021/07/04 13:54:23

//////////////////////////////////////////////////////
// String 增强
//////////////////////////////////////////////////////
// 以下是ES5的String对象，from w3c.org
// 5.1 作为函数调用 String 构造器
// 5.1.1 String ( [ value ] )
// 5.2 String 构造器
// 5.2.1 new String ( [ value ] )
// 5.3 String 构造器的属性
// 5.3.1 String.prototype
// 5.3.2 String.fromCharCode ( [ char0 [ , char1 [ , … ] ] ] )
// 5.4 字符串原型对象的属性
// 5.4.1 String.prototype.constructor
// 5.4.2 String.prototype.toString ( )
// 5.4.3 String.prototype.valueOf ( )
// 5.4.4 String.prototype.charAt (pos)
// 5.4.5 String.prototype.charCodeAt (pos)
// 5.4.6 String.prototype.concat ( [ string1 [ , string2 [ , … ] ] ] )
// 5.4.7 String.prototype.indexOf (searchString, position)
// 5.4.8 String.prototype.lastIndexOf (searchString, position)
// 5.4.9 String.prototype.localeCompare (that)
// 5.4.10 String.prototype.match (regexp)
// 5.4.11 String.prototype.replace (searchValue, replaceValue)
// 5.4.12 String.prototype.search (regexp)
// 5.4.13 String.prototype.slice (start, end)
// 5.4.14 String.prototype.split (separator, limit)
// 5.4.15 String.prototype.substring (start, end)
// 5.4.16 String.prototype.toLowerCase ( )
// 5.4.17 String.prototype.toLocaleLowerCase ( )
// 5.4.18 String.prototype.toUpperCase ( )
// 5.4.19 String.prototype.toLocaleUpperCase ( )
// 5.4.20 String.prototype.trim ( )
// 5.5 String 实例的属性
// 5.5.1 length
// 5.5.2 [[GetOwnProperty]] ( P )


function num2hex(num) {

}

var HEXMAP = {
        "0":0, '1':1, '2':2, '3':3,
        '4':4, '5':5, '6':6, '7':7,
        '8':8, '9':9, '0':0,
        'a':10, 'b':11, 'c':12, 'd':13,
        'e':14, 'f':15,
        'A':10, 'B':11, 'C':12, 'D':13,
        'E':14, 'F':15
    };

var BINMAP = {
        "0":0, '1':1, '2':2, '3':3,
        '4':4, '5':5, '6':6, '7':7,
        '8':8, '9':9, '0':0,
    };

function _strfill(len, c) {
    c = c || ' ';
    s = "";
    for(var i = 0; i < len; i++) {
        s += c;
    }
    return s;
}

function _fmtnum(numval, limit) {
    var max = Math.pow(10, limit);
    if (numval > max) {
        return "" + numval;
    } else {
        var cnt = 1;
        var num = numval;
        num /= 10;
        while (num >= 1) {
            cnt+=1;
            num /= 10;
        }
        // what if the num is negative?
        var zeros = limit - cnt;
        return _strfill(zeros, '0') + numval;
    }
}



function _fmtstr(strval, limit) {
    if (strval.length < limit) {
        return strval + _strfill(limit - strval.length);
    } else {
        strval = strval.substr(0, limit);
        return strval;
    }
}

function sFormat(fmt) {
    var dest = "";
    var idx = 1;
    var hexmap = BINMAP;
    for(var i = 0; i < fmt.length; i++) {
        var c = fmt[i];
        if (c == '%') {
            switch (fmt[i+1]) {
                case 's':
                    i+=1;
                    dest += arguments[idx];
                    idx+=1;
                    break;
                case '%':
                    i+=1;
                    dest += '%';
                    break;
                case '0':
                case '1':
                case '2':
                case '3': case '4': case '5':
                case '6': case '7': case '8':
                case '8': case '9': {
                    var num = 0;
                    i += 1;
                    while (hexmap[fmt[i]] != undefined) {
                        num = num * 10 + hexmap[fmt[i]];
                        i+=1;
                    }
                    if (fmt[i] == 'd') {
                        var val = 0;
                        try {
                            val = parseInt(arguments[idx]);
                        } catch (e) {
                            console.log(e);
                            dest += 'NaN';
                            idx+=1;
                            break;
                        }
                        idx+=1;
                        dest += _fmtnum(val, num);
                    } else if (fmt[i] == 's') {
                        dest += _fmtstr(arguments[idx], num);
                        idx+=1;
                    }
                    i+=1;
                }
                break;
                default:
                    dest += '%';
                    break;
            }
        } else {
            dest += c;
        }
    }
    return dest;
}

window.sformat = sFormat;

function hex2num(hex) {
    var hexmap = HEXMAP;
    if(hex[0] == '0' && (hex[1] == 'X' || hex[1] == 'x')) {
        hex = hex.substr(2);
    }
    var num = 0;
    for(var i = 0; i < hex.length; i++) {
        var c = hex[i];
        num = num * 16;
        if (hexmap[c] == undefined) {
            throw 'invalid char ' + c;
        } else {
            num += hexmap[c];
        }
    }
    return num;
}


function stringStartsWith(chars) {
    return this.indexOf(chars) === 0;
}

String.prototype.startsWith = String.prototype.startsWith || stringStartsWith;

String.prototype.endsWith = String.prototype.endsWith || function (ends) {
    
    function _StrEndsWith(str, ends) {
        return str.lastIndexOf(ends) === (str.length - ends.length);
        // for (var i = ends.length-1, j = str.length - 1; i >= 0; i--, j--) {
        //     if (str[j] != ends[i]) {
        //         return false;
        //     }
        // }
        // return true;
    } 
        
    if (!ends instanceof Array){
        return _StrEndsWith(this, ends);
    } else {
        for (var i = 0; i < ends.length; i++) {
            if (_StrEndsWith(this, ends[i])) {
                return true;
            }
        }
        return false;
    }
}


String.prototype.count = String.prototype.count || function (dst) {
    var count = 0;
    var start = 0;
    var index = -1;
    while ((index = this.indexOf(dst, start)) != -1) {
        count += 1;
        start = index + 1;
    }
    return count;
}

String.prototype.format = String.prototype.format || function () {
    var dest = "";
    var idx = 0;
    for(var i = 0; i < this.length; i++) {
        var c = this[i];
        if (c == '%') {
            switch (this[i+1]) {
                case 's':
                    i+=1;
                    dest += arguments[idx];
                    idx+=1;
                    break;
                case '%':
                    i+=1;
                    dest += '%';
                    break;
                default:
                    dest += '%';
                    break;
            }
        } else {
            dest += c;
        }
    }
    return dest;
}
/**
 * @param {int} count
 * @return {string}
 */
String.prototype.repeat = function (count) {
    var value = this;
    var str = "";
    for (var i = 0; i < count; i++) {
        str += value;
    }
    return str;
}

/**
 * 访问字符串的某个下标字符
 * @param {int} index
 * @return {string}
 */
String.prototype.Get = function (index) {
    if (index >= 0) {
        return this[index];
    } else {
        var realIndex = this.length + index;
        return this[realIndex];
    }
}

/**
 * 简单的模板渲染，这里假设传进来的参数已经进行了html转义
 */
function renderTemplate(templateText, object) {
    return templateText.replace(/\$\{(.*?)\}/g, function (context, objKey) {
        return object[objKey.trim()] || '';
    });
}

/**
 * 原型：字符串格式化
 * @param args 格式化参数值
 */
// String.prototype.format = function(args) {
//     var result = this;
//     if (arguments.length < 1) {
//         return result;
//     }

//     var data = arguments; // 如果模板参数是数组
//     if (arguments.length == 1 && typeof (args) == "object") {
//         // 如果模板参数是对象
//         data = args;
//     }
//     return result.replace(/\{(.*?)\}/g, function (context, objKey) {
//         return object[objKey.trim()] || '';
//     });
// }

// @author xupingmao
// @since 2017/08/16
// @modified 2020/07/04 16:41:01

/**
 * 日期格式化
 * @param {string} format 日期格式
 */
Date.prototype.format = Date.prototype.format || function (format) {
    var year = this.getFullYear();
    var month = this.getMonth() + 1;
    var day = this.getDate();
    var hour = this.getHours();
    var minute = this.getMinutes();
    var second = this.getSeconds();
    if (format == "yyyy-MM-dd") {
        return sFormat("%d-%2d-%2d", year, month, day);
    }
    if (format == "HH:mm:ss") {
        return sFormat("%2d:%2d:%2d", hour, minute, second);
    }
    return sFormat("%d-%2d-%2d %2d:%2d:%2d", year, month, day, hour, minute, second);
};

// @author xupingmao
// @since 2017/08/16
// @modified 2020/07/04 16:45:18

/** 
* 获取窗口的宽度
*/
function getWindowWidth() {
    if (window.innerWidth) {
        return window.innerWidth;
    } else {
        // For IE
        return Math.min(document.body.clientHeight, document.documentElement.clientHeight);
    }
};

function getWindowHeight() {
    if (window.innerHeight) {
        return window.innerHeight;
    } else {
        // For IE
        return Math.min(document.body.clientWidth, document.documentElement.clientWidth);
    }
};
/**
 * JQuery 扩展
 * @author xupingmao
 * @since 2021/09/19 19:41:58
 * @modified 2022/04/03 21:16:04
 * @filename jq-ext.js
 */


/**
 * 获取表单数据
 */
$.fn.extend({
    /** 获取表单的数据 **/
    "formData": function () {
        var data = {}
        $(this).find("[name]").each(function (index, element) {
            var key = $(element).attr("name");
            var value = $(element).val();
            data[key] = value;
        });

        return data;
    },

    /* 滚动到底部 */
    "scrollBottom": function() {
        if (this.length==0) {
            return;
        }
        var height = this[0].scrollHeight;
        $(this).scrollTop(height);
    }
});
/**
 * xnote全局初始化
 * @author xupingmao
 * @since 2022/01/09 16:17:02
 * @modified 2022/04/09 18:15:07
 * @filename x-init.js
 */

/** 初始化xnote全局对象 **/
if (window.xnote === undefined) {
    // 全局对象
    var xnote = {};

    // 设备信息
    xnote.device = {
        contentWidth: 0,     // 内容的宽度，包括左侧主数据和侧边栏
        contentLeftWidth: 0, // 左侧的宽度
        isMobile: false, // 是否是移动端
        isDesktop: true, // 默认是桌面端
        leftNavWidth: 0, // 左侧导航宽度
        end: 0
    };

    // 配置信息
    xnote.config = {};
    xnote.config.serverHome = "";
    
    // 内部属性
    xnote._dialogIdStack = [];

    // 常量
    xnote.MOBILE_MAX_WIDTH = 1000;
    xnote.constants = {
        MOBILE_MAX_WIDTH: 100
    };

    // 后端接口API模块
    xnote.api = {};
    // 操作动作接口
    xnote.action = {};

    // 事件相关接口
    xnote.events = {};
    // resize事件回调
    xnote.events.resizeHooks = [];

    // 表格模块
    xnote.table = {};
    // 编辑器模块
    xnote.editor = {};
    // 业务状态
    xnote.state = {};
    // 系统状态
    xnote.state.system = {};
    // 按键弹起的时间
    xnote.state.system.keyupTime = new Date().getTime();

    // http相关操作
    xnote.http = {};

    // 功能模块
    xnote.note = {};

    // 字符串模块
    xnote.string = {};
}

xnote.registerApiModule = function (name) {
    if (xnote.api[name] === undefined) {
        xnote.api[name] = {};
    }
};

/**
 * 注册API
 * @param {string} apiName API名称
 * @param {function} fn 函数
 */
xnote.registerApi = function (apiName, fn) {
    if (xnote.api[apiName] === undefined) {
        xnote.api[apiName] = fn;
    } else {
        var errMessage = "api is registered: " + apiName;
        console.error(errMessage);
        xnote.alert(errMessage);
    }
}

xnote.isEmpty = function (value) {
    return value === undefined || value === null || value === "";
};

xnote.isNotEmpty = function (value) {
    return !xnote.isEmpty(value);
};

xnote.getOrDefault = function (value, defaultValue) {
    if (value === undefined) {
        return defaultValue;
    }
    return value;
};

xnote.execute = function (fn) {
    fn();
};


xnote.validate = {
    "notUndefined": function (obj, errMsg) {
        if (obj === undefined) {
            xnote.alert(errMsg);
            throw new Error(errMsg);
        }
    },
    "isFunction": function (obj, errMsg) {
        if (typeof obj !== 'function') {
            xnote.alert(errMsg);
            throw new Error(errMsg);
        }
    }
};



// 调整表格宽度
xnote.table.adjustWidth = function(selector) {
    $(selector).each(function (element, index) {
        var headings = $(this).find("th");
        if (headings.length > 0) {
            var width = 100 / headings.length;
            headings.css("width", width + "%");
        }
    });
};

/**
 * 追加CSS样式表
 * @param {string} styleText 样式文本
 */
xnote.appendCSS = function (styleText) {
    // 居中的样式
    var style = document.createElement("style");
    style.type = "text/css";

    if (style.styleSheet) {
      // 兼容IE
      style.styleSheet.cssText = styleText;  
    } else {  
      style.innerHTML = styleText;
    } 

    document.head.appendChild(style);
};

xnote.http.defaultFailHandler = function (err) {
    console.log(err);
    xnote.toast("服务器繁忙, 请稍后重试~");
};

// http-post请求
xnote.http.post = function (url, data, callback, type) {
    return $.post(xnote.config.serverHome + url, data, callback, type).fail(xnote.http.defaultFailHandler);
}

// http-get请求
xnote.http.get = function (url, data, callback, type) {
    return $.get(xnote.config.serverHome + url, data, callback, type).fail(xnote.http.defaultFailHandler);
}

xnote.isTyping = function() {
    var now = new Date().getTime();
    var typingGap = 200; // 200毫秒
    return now - xnote.state.system.keyupTime < typingGap;
}

var XUI = function(window) {
    // 处理select标签选中情况
    function initSelect() {
        $("select").each(function(index, ele) {
            var self = $(ele);
            var children = self.children();
            // 使用$.val() 会取到第一个select标签值
            var value = self.attr("value");
            for (var i = 0; i < children.length; i++) {
                var child = children[i];
                if (value == child.value) {
                    child.selected = "selected";
                }
            }
        });
    }

    function initCheckbox() {
        $("input[type=checkbox]").each(function(index, ele) {
            var self = $(ele);
            var value = self.attr("default-value");
            if (value == "on") {
                self.attr("checked", "checked");
            }
        })
    }

    function initRadio() {
        $("input[type=radio]").each(function(index, ele) {
            var self = $(ele);
            var value = self.attr("default-value");
            if (value == self.val()) {
                self.attr("checked", "checked");
            }
        });
    }

    function initXRadio() {
        $(".x-radio").each(function(index, element) {
            var self = $(element);
            var option = self.attr("data-option");
            var value = self.attr("data-value");
            if (value == option) {
                self.addClass("selected-link");
            }
        });
    };

    // 点击跳转链接的按钮
    $(".link-btn").click(function() {
        var link = $(this).attr("x-href");
        if (!link) {
            link = $(this).attr("href");
        }
        var confirmMessage = $(this).attr("confirm-message");
        if (confirmMessage) {
            xnote.confirm(confirmMessage, function (result) {
                window.location.href = link;
            });
        } else {
            window.location.href = link;
        }
    });

    // 点击prompt按钮
    // <input type="button" class="prompt-btn" action="/rename?name=" message="重命名为" value="重命名">
    $(".prompt-btn").click(function() {
        var action = $(this).attr("action");
        var message = $(this).attr("message");
        var defaultValue = $(this).attr("default-value");
        var inputValue = prompt(message, defaultValue);
        if (inputValue != "" && inputValue) {
            var actionUrl = action + encodeURIComponent(inputValue);
            $.get(actionUrl, function(resp) {
                window.location.reload();
            })
        }
    });

    // 初始化表单控件的默认值
    function initDefaultValue(event) {
        initSelect();
        initCheckbox();
        initRadio();
        initXRadio();
        xnote.table.adjustWidth(".default-table");
    };

    window.xnote.assert = function (expression, message) {
        if (!expression) {
            xnote.alert(message);
        }
    };

    // 刷新各种默认值
    xnote.refresh = function () {
        // 初始化
        initDefaultValue();
        // 注册事件
        xnote.addEventListener("init-default-value", initDefaultValue);
        xnote.addEventListener("xnote.reload", initDefaultValue);
    };

    xnote.refresh();
};

$(document).ready(function() {
    XUI(window);
    $("body").on("keyup", function (event) {
        xnote.state.system.keyupTime = new Date().getTime();
    });
});

/**
 * 指定索引对文本进行替换
 * @param {string} text 原始文本
 * @param {string} target 被替换的文本
 * @param {string} replacement 新的文本
 * @param {int} index 索引位置
 * @returns 
 */
xnote.string.replaceByIndex = function (text, target, replacement, index) {
    var tokens = text.split(target);
    var result = [];
    for (var i = 0; i < tokens.length; i++) {
        var token = tokens[i];
        result.push(token);

        if (i+1 == tokens.length) {
            continue;
        }

        if (i == index) {
            result.push(replacement);
        } else {
            result.push(target);
        }
    }
    
    return result.join("");
};

/**
 * xnote扩展事件
 * @author xupingmao
 * @since 2021/05/30 14:39:39
 * @modified 2022/01/09 16:31:57
 * @filename x-event.js
 */

(function(){

    /**
     * 代码来自 quarkjs
     * 构造函数.
     * @name EventDispatcher
     * @class EventDispatcher类是可调度事件的类的基类，它允许显示列表上的任何对象都是一个事件目标。
     */
    var EventDispatcher = function()
    {
        //事件映射表，格式为：{type1:[listener1, listener2], type2:[listener3, listener4]}
        this._eventMap = {};
        //事件注册表，格式为: {type1:文字说明, type2:文字说明}
        this._eventDescription = {};
    };

    /**
     * 注册事件侦听器对象，以使侦听器能够接收事件通知。
     */
    EventDispatcher.prototype.addEventListener = function(type, listener)
    {
        var map = this._eventMap[type];
        if(map == null) map = this._eventMap[type] = [];
        
        if(map.indexOf(listener) == -1)
        {
            map.push(listener);
            return true;
        }
        return false;
    };

    /**
     * 删除事件侦听器。
     */
    EventDispatcher.prototype.removeEventListener = function(type, listener)
    {
        if(arguments.length == 1) return this.removeEventListenerByType(type);

        var map = this._eventMap[type];
        if(map == null) return false;

        for(var i = 0; i < map.length; i++)
        {
            var li = map[i];
            if(li === listener)
            {
                map.splice(i, 1);
                if(map.length == 0) delete this._eventMap[type];
                return true;
            }
        }
        return false;
    };

    /**
     * 删除指定类型的所有事件侦听器。
     */
    EventDispatcher.prototype.removeEventListenerByType = function(type)
    {
        var map = this._eventMap[type];
        if(map != null)
        {
            delete this._eventMap[type];
            return true;
        }
        return false;
    };

    /**
     * 删除所有事件侦听器。
     */
    EventDispatcher.prototype.removeAllEventListeners = function()
    {   
        this._eventMap = {};
    };

    /**
     * 派发事件，调用事件侦听器。
     */
    EventDispatcher.prototype.dispatchEvent = function(event)
    {
        var map = this._eventMap[event.type];
        if(map == null) return false;   
        if(!event.target) event.target = this;
        map = map.slice();

        for(var i = 0; i < map.length; i++)
        {
            var listener = map[i];
            if(typeof(listener) == "function")
            {
                listener.call(this, event);
            }
        }
        return true;
    };

    /**
     * 检查是否为指定事件类型注册了任何侦听器。
     */
    EventDispatcher.prototype.hasEventListener = function(type)
    {
        var map = this._eventMap[type];
        return map != null && map.length > 0;
    };

    /**
     * 声明一个事件，在严格模式下，如果不声明无法使用，为了避免消息过多无法管理的问题
     */
    EventDispatcher.prototype.defineEvent = function(type, description)
    {
        this._eventDescription[type] = description;
    };

    //添加若干的常用的快捷缩写方法
    EventDispatcher.prototype.on = EventDispatcher.prototype.addEventListener;
    EventDispatcher.prototype.un = EventDispatcher.prototype.removeEventListener;
    EventDispatcher.prototype.fire = EventDispatcher.prototype.dispatchEvent;

    xnote._eventDispatcher = new EventDispatcher();
    xnote.addEventListener = xnote.on = function (type, listener) {
        return xnote._eventDispatcher.addEventListener(type, listener);
    };

    xnote.dispatchEvent = xnote.fire = function (type, target) {
        var event = {type: type, target: target};
        return xnote._eventDispatcher.dispatchEvent(event);
    };
    
})();
/**
 * xnote扩展函数
 * @author xupingmao
 * @since 2021/05/30 14:39:39
 * @modified 2022/01/09 16:08:42
 * @filename x-ext.js
 */

xnote.EXT_DICT = {};

xnote.getExtFunc = function (funcName) {
    return xnote.EXT_DICT[funcName];
};

xnote.setExtFunc = function (funcName, func) {
    xnote.EXT_DICT[funcName] = func;
};
/**
 * xnote专用ui
 * 依赖库
 *   jquery
 *   layer.js
 * @author xupingmao
 * @since 2017/10/21
 * @modified 2022/04/16 20:24:02
 */

// 代码移动到 x-init.js 里面了
//源文件: https://gitee.com/sentsin/layer/blob/master/src/layer.js
//layer相册层修改版, 调整了图片大小的处理
layer.photos = function(options, loop, key){
  var cache = layer.cache||{}, skin = function(type){
    return (cache.skin ? (' ' + cache.skin + ' ' + cache.skin + '-'+type) : '');
  }; 
 
  var dict = {};
  options = options || {};
  if(!options.photos) return;
  var type = options.photos.constructor === Object;
  var photos = type ? options.photos : {}, data = photos.data || [];
  var start = photos.start || 0;
  dict.imgIndex = (start|0) + 1;

  // 状态
  dict.state = {};
  dict.state.rotate = 0; // 旋转角度
  dict.state.img = null; // 图片资源
  
  options.img = options.img || 'img';
  // 是否是移动设备
  options.isMobile = options.isMobile || false;
  
  var success = options.success;
  delete options.success;

  if(!type){ //页面直接获取
    var parent = $(options.photos);
    var pushData = function(){
      data = [];
      parent.find(options.img).each(function(index){
        var othis = $(this);
        othis.attr('layer-index', index);
        data.push({
          alt: othis.attr('alt'),
          pid: othis.attr('layer-pid'),
          src: othis.attr('layer-src') || othis.attr('src'),
          thumb: othis.attr('src')
        });
      })
    };
    
    pushData();
    
    if (data.length === 0) return;
    
    loop || parent.on('click', options.img, function(){
      var othis = $(this), index = othis.attr('layer-index'); 
      layer.photos($.extend(options, {
        photos: {
          start: index,
          data: data,
          tab: options.tab
        },
        full: options.full
      }), true);
      pushData();
    })
    
    //不直接弹出
    if(!loop) return;
    
  } else if (data.length === 0){
    return layer.msg('&#x6CA1;&#x6709;&#x56FE;&#x7247;');
  }
  
  //上一张
  dict.imgprev = function(key){
    dict.imgIndex--;
    if(dict.imgIndex < 1){
      dict.imgIndex = data.length;
    }
    dict.tabimg(key);
  };
  
  //下一张
  dict.imgnext = function(key,errorMsg){
    dict.imgIndex++;
    if(dict.imgIndex > data.length){
      dict.imgIndex = 1;
      if (errorMsg) {return};
    }
    dict.tabimg(key)
  };
  
  //方向键
  dict.keyup = function(event){
    if(!dict.end){
      var code = event.keyCode;
      event.preventDefault();
      if(code === 37){
        dict.imgprev(true);
      } else if(code === 39) {
        dict.imgnext(true);
      } else if(code === 27) {
        layer.close(dict.index);
      }
    }
  }
  
  //切换
  dict.tabimg = function(key){
    if(data.length <= 1) return;
    photos.start = dict.imgIndex - 1;
    layer.close(dict.index);
    return layer.photos(options, true, key);
    setTimeout(function(){
      layer.photos(options, true, key);
    }, 200);
  }

  // 重绘图片
  dict.repaint = function(layero) {
    console.log("layero", layero);
    var img = dict.state.img;
    var imgarea = [img.width, img.height];
    var isRotate90 = dict.state.rotate == 90 || dict.state.rotate == 270;

    if (isRotate90) {
      imgarea = [img.height, img.width];
    } 
    
    console.log("imgarea", imgarea);
    var area = dict.calcArea(imgarea, options, true);
    console.log("area", area);

    var width = area[0];
    var height = area[1];
    var top = ($(window).height() - height) / 2;
    var left = ($(window).width() - width) / 2;

    var style = {
      "width": width + "px",
      "height": height + "px",
      "left": left + "px",
      "top": top + "px",
    };

    console.log("repaint style", style);

    var imgLeft = 0;
    var imgTop = 0;

    if (isRotate90) {
      // transform是在定位确认之后以元素中心旋转
      // 所以旋转90的定位还是按照旋转之前的位置计算
      imgLeft = ($(window).width()-height)/2;
      imgTop = ($(window).height()-width)/2;
    }

    var imgCss = {
      "position": "relative",
      "width": "100%",
      "left": 0,
      "top": 0
    };

    if (isRotate90) {
      imgCss = {
        "position": "fixed",
        "width": height,
        "left": imgLeft,
        "top": imgTop
      };
    }

    console.log("img css", imgCss);

    // 渲染样式
    layero.css(style);
    layero.find(".layui-layer-content").css("height", height);
    layero.find("img").css(imgCss);
  }

  // 计算图片大小
  dict.calcArea = function (imgarea, options, returnNumber) {
    var winarea;

    if (options.isMobile) {
      // 移动端不需要预留空间，直接填满屏幕即可
      // 64是上下控制栏各32px
      winarea = [$(window).width(), $(window).height()-64];
    } else {
      winarea = [$(window).width() - 100, $(window).height() - 100];
    }
    
    //如果 实际图片的宽或者高比 屏幕大（那么进行缩放）
    if(!options.full && (imgarea[0]>winarea[0]||imgarea[1]>winarea[1])){
      var wh = [imgarea[0]/winarea[0],imgarea[1]/winarea[1]];//取宽度缩放比例、高度缩放比例
      if(wh[0] > wh[1]){//取缩放比例最大的进行缩放
        imgarea[0] = imgarea[0]/wh[0];
        imgarea[1] = imgarea[1]/wh[0];
      } else if(wh[0] < wh[1]){
        imgarea[0] = imgarea[0]/wh[1];
        imgarea[1] = imgarea[1]/wh[1];
      }
    }

    // 图片太小了，进行放大
    var minsize = 150;
    if (imgarea[0] < minsize && imgarea[1] < minsize) {
      var ratio = Math.min(minsize/imgarea[0], minsize/imgarea[1]);
      imgarea[0] = imgarea[0]*ratio;
      imgarea[1] = imgarea[1]*ratio;
    }

    if (returnNumber) {
      return imgarea;
    }
    
    return [imgarea[0]+'px', imgarea[1]+'px']; 
  }
  
  //一些动作
  dict.event = function(layero){
    
    // layer默认的行为
    // dict.bigimgPic.hover(function(){
    //   dict.imgsee.show();
    // }, function(){
    //   dict.imgsee.hide();
    // });

    dict.bigimgPic.click(function() {
      dict.imgsee.toggle();
    });

    // dict.imgsee.show();
    // $(".layui-layer-imgprev").css("position", "fixed");
    // $(".layui-layer-imgnext").css("position", "fixed");
    
    dict.bigimg.find('.layui-layer-imgprev').on('click', function(event){
      event.preventDefault();
      dict.imgprev();
    });  
    
    dict.bigimg.find('.layui-layer-imgnext').on('click', function(event){     
      event.preventDefault();
      dict.imgnext();
    });

    dict.bigimg.find(".close-span").on("click", function(event) {
      layer.close(dict.index);
    });

    dict.bigimg.find(".rotate-span").on("click", function(event) {
      dict.state.rotate += 90;
      dict.state.rotate %= 360;
      dict.bigimg.find("img").css("transform", "rotate(" + dict.state.rotate + "deg)");
      // 重新绘制弹窗
      dict.repaint(layero);
    })
    
    $(document).on('keyup', dict.keyup);

    // 触控事件
    var hammer = options.hammer;
    if (hammer) {
      hammer.on('swipeleft', function(e) {
        dict.imgprev();
      });
      hammer.on('swiperight', function(e) {
        dict.imgnext();
      });
    }
  };
  
  //图片预加载
  function loadImage(url, callback, error) {   
    var img = new Image();
    img.src = url; 
    if(img.complete){
      return callback(img);
    }
    img.onload = function(){
      img.onload = null;
      callback(img);
    };
    img.onerror = function(e){
      img.onerror = null;
      error(e);
    };  
  };
  
  dict.loadi = layer.load(1, {
    shade: 'shade' in options ? false : 0.9,
    scrollbar: false
  });

  function imgBarTop() {
    if (options.hideBar) {
      return "";
    }
    var bar = $("<div>").addClass("layui-layer-imgbar").addClass("imgbar-top").hide();

    // 旋转图片功能
    bar.append($("<span>").addClass("rotate-span").addClass("clickable").text("旋转"));
    bar.append("&nbsp;");

    var rightBox = $("<div>").addClass("float-right");
    rightBox.append($("<span>").addClass("close-span").addClass("clickable").text("关闭"));

    bar.append(rightBox);
    return bar.prop("outerHTML");
  }

  function imgBarBottom() {
    if (options.hideBar) {
      return "";
    }
    return '<div class="layui-layer-imgbar imgbar-bottom" style="display:'
      + (key ? 'block' : '') 
      + '"><span class="layui-layer-imgtit"><a target="_blank" href="' 
      + data[start].src +  '">'+ (data[start].alt||'') 
      + '</a><em>'+ dict.imgIndex +'/'+ data.length +'</em></span></div>';
  }

  loadImage(data[start].src, function(img){
    // 存储图像资源
    dict.state.img = img;

    layer.close(dict.loadi);
    dict.index = layer.open($.extend({
      type: 1,
      id: 'layui-layer-photos',
      area: dict.calcArea([img.width, img.height], options),
      title: false,
      shade: 0.9,
      shadeClose: true,
      closeBtn: false,
      // move: '.layui-layer-phimg img',
      move: false,
      moveType: 1,
      scrollbar: false,
      // 是否移出窗口
      moveOut: false,
      // anim: Math.random()*5|0,
      isOutAnim: false,
      skin: 'layui-layer-photos' + skin('photos'),
      content: '<div class="layui-layer-phimg">'
        +imgBarTop()
        +'<img src="'+ data[start].src +'" alt="'+ (data[start].alt||'') +'" layer-pid="'+ data[start].pid +'">'
        +'<div class="layui-layer-imgsee">'
          +(data.length > 1 ? '<span class="layui-layer-imguide"><a href="javascript:;" class="layui-layer-iconext layui-layer-imgprev"></a><a href="javascript:;" class="layui-layer-iconext layui-layer-imgnext"></a></span>' : '')
          +imgBarBottom()
        +'</div>'
      +'</div>',
      success: function(layero, index){
        dict.bigimg = layero.find('.layui-layer-phimg');
        dict.bigimgPic = layero.find('.layui-layer-phimg img');
        dict.imgsee = layero.find(".layui-layer-imgbar");

        // 左右方向图标始终展示
        layero.find(".layui-layer-imgnext,.layui-layer-imgprev").
          css("position", "fixed").show();
        layero.find(".layui-layer-imguide").show();
        layero.find(".layui-layer-imgbar").show();

        dict.event(layero);
        options.tab && options.tab(data[start], layero);
        typeof success === 'function' && success(layero);
      }, end: function(){
        dict.end = true;
        $(document).off('keyup', dict.keyup);
      }
    }, options));
  }, function(){
    layer.close(dict.loadi);
    layer.msg('&#x5F53;&#x524D;&#x56FE;&#x7247;&#x5730;&#x5740;&#x5F02;&#x5E38;<br>&#x662F;&#x5426;&#x7EE7;&#x7EED;&#x67E5;&#x770B;&#x4E0B;&#x4E00;&#x5F20;&#xFF1F;', {
      time: 30000, 
      btn: ['&#x4E0B;&#x4E00;&#x5F20;', '&#x4E0D;&#x770B;&#x4E86;'], 
      yes: function(){
        data.length > 1 && dict.imgnext(true,true);
      }
    });
  });
};
(function () {

/** 
* 获取窗口的宽度
*/
xnote.getWindowWidth = function() {
    if (window.innerWidth) {
        return window.innerWidth;
    } else {
        // For IE
        return Math.min(document.body.clientHeight, document.documentElement.clientHeight);
    }
}

window.getWindowWidth = xnote.getWindowWidth;

// 获取窗口的高度
xnote.getWindowHeight = function() {
    if (window.innerHeight) {
        return window.innerHeight;
    } else {
        // For IE
        return Math.min(document.body.clientWidth, document.documentElement.clientWidth);
    }
}

window.getWindowHeight = xnote.getWindowHeight

/**
 * 判断是否是PC设备，要求width>=800 && height>=600
 */
xnote.isDesktop = function() {
    return getWindowWidth() >= 800;
}

// alias
window.isPc = xnote.isDesktop;
window.isDesktop = window.isDesktop;

window.isMobile = function() {
    return !isPc();
};

xnote.isMobile = function() {
    return $(window).width() < xnote.MOBILE_MAX_WIDTH;
};



/**
 * 浏览器的特性的简单检测，并非精确判断。
 * from quark.js
 */
function detectBrowser(ns)
{
    var win = window;
	var ua = ns.ua = navigator.userAgent;		
	ns.isWebKit = (/webkit/i).test(ua);
	ns.isMozilla = (/mozilla/i).test(ua);	
	ns.isIE = (/msie/i).test(ua);
	ns.isFirefox = (/firefox/i).test(ua);
	ns.isChrome = (/chrome/i).test(ua);
	ns.isSafari = (/safari/i).test(ua) && !this.isChrome;
	ns.isMobile = (/mobile/i).test(ua);
	ns.isOpera = (/opera/i).test(ua);
	ns.isIOS = (/ios/i).test(ua);
	ns.isIpad = (/ipad/i).test(ua);
	ns.isIpod = (/ipod/i).test(ua);
	ns.isIphone = (/iphone/i).test(ua) && !this.isIpod;
	ns.isAndroid = (/android/i).test(ua);
	ns.supportStorage = "localStorage" in win;
	ns.supportOrientation = "orientation" in win;
	ns.supportDeviceMotion = "ondevicemotion" in win;
	ns.supportTouch = "ontouchstart" in win;
	ns.supportCanvas = document.createElement("canvas").getContext != null;
	ns.cssPrefix = ns.isWebKit ? "webkit" : ns.isFirefox ? "Moz" : ns.isOpera ? "O" : ns.isIE ? "ms" : "";
};

detectBrowser(xnote.device);

})();/** 下拉组件
 * @since 2020/01/11
 * @modified 2020/01/22 00:29:27
 */


// jquery 扩展
$.fn.extend({
    "hideDropdown": function () {
        var self = $(this);
        if (self.hasClass("mobile")) {
            self.animate({
                "height": "0px"
            }).removeClass("active");
            self.parent().find(".dropdown-mask").hide();
            xnote.enableBodyScroll();
        } else {
            self.slideUp("fast");
        }
    }
});


xnote.disableBodyScroll = function (e) {
    // preventDefault 不能完全阻止滚动
    $("body").css("overflow", "hidden");
}

xnote.enableBodyScroll = function (e) {
    $("body").css("overflow", "auto");
}

xnote.showDropdown = function (target) {
    var dropdownContent = $(target).siblings(".dropdown-content");
    if (dropdownContent.hasClass("mobile")) {
        console.log("dropdown mobile");
        // 移动端动画
        if (dropdownContent.hasClass("active")) {
            // 已经展示了
            return;
        } else {
            // 隐藏 -> 展示
            $(target).parent().find(".dropdown-mask").show();
            dropdownContent.show().animate({
                "height": "60%"
            }).addClass("active");
            xnote.disableBodyScroll();
        }
    } else {
        dropdownContent.slideDown("fast");
        if (dropdownContent.offset() && dropdownContent.offset().left < 0) {
            dropdownContent.css("left", 0);
        }
    }
}

xnote.toggleDropdown = function (target) {
    var dropdownContent = $(target).siblings(".dropdown-content");
    if (dropdownContent.hasClass("mobile")) {
        console.log("dropdown mobile");
        // 移动端动画
        if (dropdownContent.hasClass("active")) {
            // 展示 -> 隐藏
            dropdownContent.hideDropdown();
        } else {
            // 隐藏 -> 展示
            $(target).parent().find(".dropdown-mask").show();
            dropdownContent.show().animate({
                "height": "60%"
            }).addClass("active");
            xnote.disableBodyScroll();
        }
    } else {
        dropdownContent.slideToggle("fast");
        if (dropdownContent.offset() && dropdownContent.offset().left < 0) {
            dropdownContent.css("left", 0);
        }

        // 关闭非当前的dropdown
        $(".dropdown-content").each(function (index, element) {
            if (element != dropdownContent[0]) {
                $(element).slideUp(0);
            }
        });
    }
}

$(function () {
    $(".dropdown").click(function (e) {
        xnote.toggleDropdown(e.target);
    });

    $(".x-dropdown").click(function (e) {
        xnote.toggleDropdown(e.target);
    });

    $("body").on("click", function (e) {
        var target = e.target;
        if ($(target).hasClass("dropdown") || $(target).hasClass("dropdown-btn")) {
            return;
        }
        $(".dropdown-content").hideDropdown();
    });

});

/** 图片处理 part of xnote-ui 
 * @filename x-photo.js
 */

$(function () {
  // 图片处理
  $("body").on('click', ".x-photo", function (e) {
        // console.log(e);
        var src = $(this).attr("src");
        var alt = $(this).attr("alt");
        console.log(src);

        var data = [];
        var imageIndex = 0;
        var target = e.target;

        $(".x-photo").each(function(index, el) {
          if (el == target) {
            imageIndex = index;
          }

          var src = $(el).attr("data-src");
          if (!src) {
            src = $(el).attr("src");
          }
          
          data.push({
            "alt": $(el).attr("alt"),
            "pid": 0,
            "src": src,
            "thumb": ""
          });
        });

        // 触控接口
        var hammer;
        if (window.Hammer) {
          hammer = new Hammer(document.body);
        }

        layer.photos({
            "photos": {
                  "title": "", //相册标题
                  "id": 123,   //相册id
                  "start": imageIndex, //初始显示的图片序号，默认0
                  "data": data
                },
            "anim":5,
            "hideBar": false,
            "isMobile": xnote.isMobile(),
            "hammer": hammer,
        });
  });
});
/** audio.js, part of xnote-ui 
 * @since 2020/01/05
 * @modified 2022/01/09 16:09:02
 **/

$(function(e) {

    // 默认不启用
    var audioEnabled = false;

    $("body").on("click", ".x-audio", function(e) {
        var src = $(this).attr("data-src");
        layer.open({
            type: 2,
            content: src,
            shade: 0
        });
    });

    var AUDIO_MAP = {};

    xnote.loadAudio = function (id, src) {
        AUDIO_MAP[id] = new Audio(src);
    }

    xnote.playAudio = function (id) {
        if (!audioEnabled) {
            return;
        }

        var audioObject = AUDIO_MAP[id];
        if (audioObject) {
            audioObject.play();
        }
    }

});
/**
 * xnote的公有方法
 */

var BASE_URL = "/static/lib/webuploader";

function createXnoteLoading() {
    return loadingIndex = layer.load(2);
}

function closeXnoteLoading(index) {
    layer.close(index);
}

xnote._initUploadEvent = function(uploader, fileSelector, successFn) {
    // 加载进度条索引
    var loadingIndex = 0;

    // 当有文件添加进来的时候
    uploader.on( 'fileQueued', function( file ) {
        // 接受文件
    });


    // 文件上传过程中创建进度条实时显示。
    uploader.on( 'uploadProgress', function( file, percentage ) {
        var percent = (percentage * 100).toFixed(2) + '%';
        console.log('upload process ' + percent)
    });

    uploader.on( 'uploadBeforeSend', function (object, data, headers) {
        $( '#uploadProgress' ).find('.progress').remove();
        data.dirname = "auto";
    })

    // 文件上传成功，给item添加成功class, 用样式标记上传成功。
    uploader.on( 'uploadSuccess', function( file, resp) {
        layer.close(loadingIndex);
        successFn(resp);
    });

    // 文件上传失败，显示上传出错。
    uploader.on( 'uploadError', function( file ) {
        console.error("uploadError", file);
        layer.close(loadingIndex);
        layer.alert('上传失败');
    });

    // 完成上传完了，成功或者失败，先删除进度条。
    uploader.on( 'uploadComplete', function( file ) {
        
    });

    // 监听文件上传事件
    $(fileSelector).on("change", function (event) {
        console.log(event);
        var fileList = event.target.files; //获取文件对象 
        if (fileList && fileList.length > 0) {
            loadingIndex = layer.load(2);
            uploader.addFile(fileList);
        }
    });
};

xnote.createUploader = function(fileSelector, chunked, successFn) {
    var req = {
        fileSelector: fileSelector,
        chunked: chunked,
        successFn: successFn,
        fixOrientation: true
    }

    if (chunked) {
        req.fixOrientation = false;
    }

    return xnote.createUploaderEx(req);
}

/** 创建上传器 **/
xnote.createUploaderEx = function(req) {
    var fileSelector = req.fileSelector;
    var chunked = req.chunked;
    var successFn = req.successFn;
    var fixOrientation = req.fixOrientation;


    if (fileSelector == undefined) {
        fileSelector = '#filePicker';
    }

    var upload_service;
    var serverHome = xnote.config.serverHome;

    // 默认分片
    if (chunked == undefined) {
        chunked = false;
    }

    if (chunked) {
        upload_service = serverHome + "/fs_upload/range";
    } else {
        // 不分片的上传服务
        upload_service = serverHome + "/fs_upload";
    }

    var uploader = WebUploader.create({
        // 选完文件后，是否自动上传。
        auto: true,
        // swf文件路径
        swf: BASE_URL + '/Uploader.swf',
        // 文件接收服务端。
        server: upload_service,
        // 选择文件的按钮。可选。
        // 内部根据当前运行是创建，可能是input元素，也可能是flash.
        pick: fileSelector,
        // 需要分片
        chunked: chunked,
        // 默认5M
        // chunkSize: 1024 * 1024 * 5,
        chunkSize: 1024 * 1024 * 5,
        // 重试次数
        chunkRetry: 10,
        // 文件上传域的name
        fileVal: "file",
        // 不开启并发
        threads: 1,
        // 是否保留header信息
        preserveHeaders: true,
        // 默认压缩是开启的
        // compress: {}
    });

    uploader.on('uploadBeforeSend', function(object, data, headers) {
        // web-uploader在上传文件的时候会自动进行旋转，但是不处理extif
        data.fix_orientation = fixOrientation;
    });

    if (successFn) {
        xnote._initUploadEvent(uploader, fileSelector, successFn);
    }

    return uploader;
};

// 把blob对象转换成文件上传到服务器
xnote.uploadBlob = function(blob, prefix, successFn, errorFn) {
    var fd = new FormData();
    // 加载页，用户阻止用户交互
    var loadingIndex = createXnoteLoading();

    fd.append("file", blob);
    fd.append("prefix", prefix);
    fd.append("name", "auto");
    //创建XMLHttpRequest对象
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/fs_upload');
    xhr.onload = function() {
        closeXnoteLoading(loadingIndex);
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                if (successFn) {
                    successFn(data);
                } else {
                    console.log(data);
                }
            } else {
                console.error(xhr.statusText);
                if (errorFn) {
                    errorFn(xhr);
                }
            }
        };
    };

    xhr.onerror = function(error) {
        console.log(xhr.statusText);
        closeXnoteLoading(loadingIndex);
        if (errorFn) {
            errorFn(error)
        }
    }
    xhr.send(fd);
};

xnote.requestUpload = function(fileSelector, chunked, successFn, errorFn) {
    if (fileSelector == undefined) {
        throw new Error("selector is undefined");
    }

    var loadingIndex = 0;
    var uploader = window.xnote.createUploader(fileSelector, chunked);

    // 当有文件添加进来的时候
    uploader.on('fileQueued', function(file) {
        // 添加文件
        console.log("file = " + file);
    });

    // 文件上传过程中创建进度条实时显示。
    uploader.on('uploadProgress', function(file, percentage) {
        // 进度条
    });

    uploader.on('uploadBeforeSend', function(object, data, headers) {
        data.dirname = "auto";
    });

    // 文件上传成功，给item添加成功class, 用样式标记上传成功。
    uploader.on('uploadSuccess', function(file, resp) {
        console.log("uploadSuccess", file, resp);

        // 关闭加载页
        closeXnoteLoading(loadingIndex);
        // 回调成功函数
        successFn(resp);
    });

    // 文件上传失败，显示上传出错。
    uploader.on('uploadError', function(file) {
        layer.alert('上传失败');
        // 关闭加载页
        closeXnoteLoading(loadingIndex);
    });

    // 完成上传完了，成功或者失败，先删除进度条。
    uploader.on('uploadComplete', function(file) {
        console.log("uploadComplete", typeof(file), file);
    });

    // 触发上传文件操作
    $(fileSelector).click();

    // 选择文件完毕
    $(fileSelector).on("change", function(event) {
        console.log(event);
        var fileList = event.target.files; //获取文件对象 
        if (fileList && fileList.length > 0) {
            uploader.addFile(fileList);
            // 创建加载页，阻止用户操作
            loadingIndex = createXnoteLoading();
        }
        // 清空文件列表，不然下次上传会重复
        event.target.files = [];
    });
};

// 通过剪切板请求上传
// @param {event} e 粘贴事件
// @param {string} filePrefix 保存的文件名前缀
// @param {function} successFn 成功的回调函数
// @param {function} errorFn 失败的回调函数
window.xnote.requestUploadByClip = function (e, filePrefix, successFn, errorFn) {
    console.log(e);
    var clipboardData = e.clipboardData || e.originalEvent 
        && e.originalEvent.clipboardData || {};

    // console.log(clipboardData);
    if (clipboardData.items) {
        items = clipboardData.items;
        for (var index = 0; index < items.length; index++) {
            var item  = items[index];
            var value = item.value;
            // console.log("requestUploadByClip", item, value);
            if (/image/i.test(item.type)) {
                console.log(item);

                // 取消默认的粘贴动作（默认会粘贴文本）
                e.preventDefault();

                // 创建加载页，阻止用户操作
                var loadingIndex = createXnoteLoading();

                var blob = item.getAsFile();
                xnote.uploadBlob(blob, filePrefix, function (resp) {
                    successFn(resp);
                    closeXnoteLoading(loadingIndex);
                }, function (resp) {
                    if (errorFn) {
                        errorFn(resp);
                    }
                    closeXnoteLoading(loadingIndex);
                });
            }
        }
    }
}

/** x-upload.js end **/
/** 
 * 对话框实现
 * 参考 https://www.layui.com/doc/modules/layer.html
 * 
 * 对外接口:
 * 1. 展示对话框并且自适应设备
 *    xnote.showDialog(title, html, buttons = [], functions = [])
 *    xnote.openDialog(title, html, buttons = [], functions = [])
 *    xnote.showDialogEx(options)
 * 
 * 2. 展示iframe页面
 *    xnote.showIframeDialog(title, url)
 *    xnote.showAjaxDialog(title, url, buttons, functions)
 * 
 * 3. 展示选项的对话框
 *    // option参数的定义 {html, title = false}
 *    xnote.showOptionDialog(option)
 * 
 * 4. 系统自带的弹窗替换
 *    xnote.alert(message)
 *    xnote.confirm(message, callback)
 *    xnote.prompt(title, defaultValue, callback)
 *    // 打开文本编辑的对话框
 *    xnote.showTextDialog(title, text, buttons, functions)
 *    xnote.openTextDialog(title, text, buttons, functions)
 * 
 */


if (window.xnote === undefined) {
    throw new Error("xnote is undefined!");
}

xnote.getDialogArea = function () {
    if (isMobile()) {
        return ['100%', '100%'];
    } else {
        return ['600px', '80%'];
    }
}

getDialogArea = xnote.getDialogArea;

xnote.getDialogAreaLarge = function() {
    if (xnote.isMobile()) {
        return ['100%', '100%'];
    } else {
        return ['80%', '80%'];
    }
}

xnote.getDialogAreaFullScreen = function() {
    return ["100%", "100%"];
}

xnote.getNewDialogId = function () {
    var dialogId = xnote.state._dialogId;
    if (dialogId === undefined) {
        dialogId = 1;
    } else {
        dialogId++;
    }
    xnote.state._dialogId = dialogId;
    return "_xnoteDialog" + dialogId;
}

xnote.showIframeDialog = function (title, url, buttons, functions) {
    var area = getDialogArea();
    return layer.open({
        type: 2,
        shadeClose: false,
        title: title,
        maxmin: true,
        area: area,
        content: url,
        scrollbar: false,
        btn: buttons,
        functions: functions
    });
}

// 关闭对话框的入口方法
xnote.closeDialog = function (flag) {
    if (flag === "last") {
        var lastId = xnote._dialogIdStack.pop();
        layer.close(lastId);
    }

    if (typeof(flag) === 'number') {
        layer.close(flag);
        // TODO 移除_dialogIdStack中的元素
    }
}

xnote.openDialogEx = function (options) {
    var dialogId = xnote.openDialogExInner(options);
    xnote._dialogIdStack.push(dialogId);
    return dialogId;
}

xnote.showDialogEx = function () {
    return xnote.openDialogEx.apply(this, arguments);
}

/**
 * 创建对话框
 * @param {object} options 创建选项
 * @param {string} options.title 标题
 * @param {string} options.html HTML内容
 * @param {list[string]} options.buttons 按钮文案
 * @param {list[function]} options.functions 回调函数(第一个是成功的回调函数)
 * @param {boolean} options.closeForYes 成功后是否关闭对话框(默认关闭)
 * @returns index
 */
xnote.openDialogExInner = function (options) {
    var area = options.area;
    var title = options.title;
    var html  = options.html;
    var buttons = options.buttons;
    var functions = options.functions;
    var anim = options.anim;
    var closeBtn = options.closeBtn;
    var onOpenFn = options.onOpenFn;
    var shadeClose = xnote.getOrDefault(options.shadeClose, false);
    var closeForYes = xnote.getOrDefault(options.closeForYes, true);
    var template = options.template;
    var defaultValues = options.defaultValues; // 模板的默认值
    var yesFunction = function(index, layero, dialogInfo) {};
    var successFunction = function(layero, index, that/*原型链的this对象*/) {};

    // 详细文档 https://www.layui.com/doc/modules/layer.html
    // @param {int} anim 动画的参数
    // undefined: 默认动画
    // 0：平滑放大。默认
    // 1：从上掉落
    // 2：从最底部往上滑入
    // 3：从左滑入
    // 4：从左翻滚
    // 5：渐显
    // 6：抖动出现

    if (template !== undefined && html !== undefined) {
        throw new Error("不能同时设置template和html选项");
    }

    var dialogId = "";

    if (template !== undefined) {
        var templateBody = $(template).html();
        dialogId = xnote.getNewDialogId();

        var ele = $("<div>").attr("id", dialogId).html(templateBody);
        html = ele.prop("outerHTML");

        if (defaultValues !== undefined) {
            html = xnote.renderTemplate(html, defaultValues); 
        }
    }

    if (functions === undefined) {
        functions = [];
    }

    if (!(functions instanceof Array)) {
        functions = [functions];
    }

    if (functions.length>0) {
        yesFunction = functions[0];
    }

    if (area === undefined) {
        area = xnote.getDialogArea();
    }

    if (area == "large") {
        area = xnote.getDialogAreaLarge();
    }

    if (area == "fullscreen") {
        area = xnote.getDialogAreaFullScreen();
    }

    var params = {
        type: 1,
        title: title,
        shadeClose: shadeClose,
        closeBtn: closeBtn,
        area: area,
        content: html,
        anim: anim,
        success: successFunction,
        // scrollbar是弹层本身的滚动条，不是整个页面的
        scrollbar: false
    }

    if (buttons !== undefined) {
        params.btn = buttons
        params.yes = function (index, layero) {
            console.log(index, layero);
            var dialogInfo = {
                id: dialogId
            };
            var yesResult = yesFunction(index, layero, dialogInfo);
            if (yesResult === undefined && closeForYes) {
                layer.close(index);
            }
            return yesResult;
        }
    }

    var index = layer.open(params);

    // 打开对话框的回调
    if (onOpenFn) {
        onOpenFn(index);
    }
    return index
}

/**
 * 打开一个对话框
 * @param {string} title 标题
 * @param {string|DOM} html 文本或者Jquery-DOM对象 比如 $(".mybox")
 * @param {array} buttons 按钮列表
 * @param {array} functions 函数列表
 * @returns 弹层的索引
 */
xnote.openDialog = function(title, html, buttons, functions) {
    var options = {};
    options.title = title;
    options.html  = html;
    options.buttons = buttons;
    options.functions = functions;
    return xnote.showDialogEx(options);
}

xnote.showDialog = function () {
    return xnote.openDialog.apply(this, arguments);
}

// 打开文本对话框
xnote.openTextDialog = function(title, text, buttons, functions, features) {
    var req = {};
    req.title = title;
    req.html  = $("<textarea>").addClass("dialog-textarea").text(text).prop("outerHTML");
    req.buttons = buttons;
    req.functions = functions;
    if (features != undefined) {
        xnote._updateDialogFeatures(req, features);
    }
    return xnote.showDialogEx(req);
}

xnote._updateDialogFeatures = function (options, features) {
    for (var i = 0; i < features.length; i++) {
        var item = features[i];
        if (item === "large") {
            options.area = "large";
        }
    }
}

// 别名
xnote.showTextDialog = xnote.openTextDialog;

/**
 * 打开ajax对话框
 * @param {object} options 打开选项
 */
xnote.openAjaxDialogEx = function (options) {
    var respFilter = xnote.getOrDefault(options.respFilter, function (resp) {
        return resp;
    });

    $.get(options.url, function (resp) {
        options.html = respFilter(resp);
        xnote.showDialogEx(options);
        // 刷新各种组件的默认值
        xnote.refresh();
    }).fail(function (error) {
        xnote.alert("调用接口失败，请重试");
    });
}

/**
 * 打开ajax对话框
 * @param {string} title 对话框标题
 * @param {string} url 对话框URL
 * @param {list<string>} buttons 按钮名称
 * @param {list<function>} functions 按钮对应的函数
 */
xnote.openAjaxDialog = function(title, url, buttons, functions) {
    var options = {};
    options.title = title;
    options.buttons = buttons;
    options.functions = functions;
    options.url = url;
    
    return xnote.openAjaxDialogEx(options);
}

// 函数别名
xnote.showAjaxDialog = function () {
    return xnote.openAjaxDialog.apply(this, arguments);
}

// 询问函数，原生prompt的替代方案
xnote.prompt = function(title, defaultValue, callback) {
    if (layer && layer.prompt) {
        // 使用layer弹层
        layer.prompt({
            title: title,
            value: defaultValue,
            scrollbar: false,
            area: ['400px', '300px']
        },
        function(value, index, element) {
            callback(value);
            layer.close(index);
        })
    } else {
        // 使用系统默认的prompt
        var result = prompt(title, defaultValue);
        callback(result);
    }
};

// 确认函数
xnote.confirm = function(message, callback) {
    if (layer && layer.confirm) {
        layer.confirm(message,
        function(index) {
            callback(true);
            layer.close(index);
        });
    } else {
        var result = confirm(message);
        callback(result);
    }
};

// 警告函数
xnote.alert = function(message) {
    if (layer && layer.alert) {
        layer.alert(message);
    } else {
        alert(message);
    }
};

/**
 * 展示Toast信息
 * @param {string} message 展示信息
 * @param {number} time 显示时间
 * @param {function} callback 回调函数
 */
xnote.toast = function (message, time, callback) {
    if (layer && layer.msg) {
        layer.msg(message, {time: time});
    } else {
        myToast(message, time);
    }

    if (callback) {
        if (time === undefined) {
            time = 1000;
        }
        setTimeout(callback, time);
    }
}

var myToast = function(message, timeout) {
    if (timeout == undefined) {
        timeout = 1000;
    }
    var maxWidth = $(document.body).width();
    var maxHeight = $(document.body).height()
    var fontSize = 14;
    var toast = $("<div>").css({
        "margin": "0 auto",
        "position": "fixed",
        "left": 0,
        "top": "24px",
        "font-size": fontSize,
        "padding": "14px 18px",
        "border-radius": "4px",
        "background": "#000",
        "opacity": 0.7,
        "color": "#fff",
        "line-height": "22px",
        "z-index": 1000
    });
    toast.text(message);

    $(document.body).append(toast);

    // 宽度
    var width = toast.outerWidth();
    var left = (maxWidth - width) / 2;
    if (left < 0) {
        left = 0;
    }
    toast.css("left", left);

    // 高度
    var height = toast.outerHeight();
    var top = (maxHeight - height) / 2;
    if (top < 0) {
        top = 0;
    }
    toast.css("top", top);

    setTimeout(function() {
        toast.remove();
    }, timeout);
}

// 兼容之前的方法
window.showToast = window.xnote.toast;

/**
 * 展示选项对话框
 */
xnote.showOptionDialog = function (option) {
    var content = option.html;
    if (option.title === undefined) {
        option.title = false;
    }

    var oldStyle = $("body").css("overflow");
    $("body").css("overflow", "hidden");

    function recoveryStyle() {
        $("body").css("overflow", oldStyle);
    }

    var dialogIndex = layer.open({
        title: option.title,
        closeBtn: false,
        shadeClose: true,
        btn: [],
        content: content,
        skin: "x-option-dialog",
        yes: function (index, layero) {
            layer.close(index);
            // 恢复样式
            recoveryStyle();
        },
        cancel: function() {
            layer.close(index);
            // 恢复样式
            recoveryStyle();
        }
    });

    // 原组件点遮罩关闭没有回调事件，要重新一下
    $('#layui-layer-shade'+ dialogIndex).on('click', function(){
        console.log("xnote.showOptionDialog: shadowClose event")
        layer.close(dialogIndex);
        recoveryStyle();
    });
};

// 老版本的对话框，先保留在这里
window.ContentDialog = {
  open: function (title, content, size) {
    var width = $(".root").width() - 40;
    var area;

    if (isMobile()) {
      area = ['100%', '100%'];
    } else {
      if (size == "small") {
        area = ['400px', '300px'];        
      } else {
        area = [width + 'px', '80%'];
      }
    }

    layer.open({
      type: 1,
      shadeClose: true,
      title: title,
      area: area,
      content: content,
      scrollbar: false
    });
  }
}

xnote.closeAllDialog = function() {
    layer.closeAll();
}


// 自定义的dialog
$(function () {

    // 点击激活对话框的按钮
    $("body").on("click", ".dialog-btn", function() {
        var dialogUrl = $(this).attr("dialog-url");
        var dialogId = $(this).attr("dialog-id");
        var dailogTitle = $(this).attr("dialog-title");
        var optionSelector = $(this).attr("dialog-option-selector");
        if (dialogUrl) {
            // 通过新的HTML页面获取dialog
            $.get(dialogUrl, function(respHtml) {

                // 展示对话框
                xnote.showDialog(dailogTitle, respHtml);

                // 重新绑定事件
                xnote.fire("init-default-value");
            })
        } else if (optionSelector) {
            var html = $(optionSelector).html();
            var option = {};
            option.html = html;
            xnote.showOptionDialog(option);
        } else {
            xnote.alert("请定义[dialog-url]或者[dialog-option-selector]属性");
        }
    });


    /**
     * 初始化弹层
     */
    function initDialog() {
        // 初始化样式
        $(".x-dialog-close").css({
            "background-color": "red",
            "float": "right"
        });

        $(".x-dialog").each(function(index, ele) {
            var self = $(ele);
            var width = window.innerWidth;
            if (width < 600) {
                dialogWidth = width - 40;
            } else {
                dialogWidth = 600;
            }
            var top = Math.max((getWindowHeight() - self.height()) / 2, 0);
            var left = (width - dialogWidth) / 2;
            self.css({
                "width": dialogWidth,
                "left": left
            }).css("top", top);
        });

        $("body").css("overflow", "hidden");
    }

    /** 隐藏弹层 **/
    function onDialogHide() {
        $(".x-dialog").hide();
        $(".x-dialog-background").hide();
        $(".x-dialog-remote").remove(); // 清空远程的dialog
        $("body").css("overflow", "auto");
    }

    $(".x-dialog-background").click(function() {
        onDialogHide();
    });

    $(".x-dialog-close, .x-dialog-cancel").click(function() {
        onDialogHide();
    });

    function doModal(id) {
        initDialog();
        $(".x-dialog-background").show();
        $(".x-dialog-remote").show();
        $("#" + id).show();
    }

    xnote.initDialog = initDialog;
});
/** x-tab.js
 * tab页功能，依赖jQuery
 * 有两个样式: tab-link 和 tab-btn
 */

$(function (e) {

    function initTabBtn() {
        var hasActive = false;
        var count = 0;
        var pathAndSearch = location.pathname + location.search;

        $(".x-tab-btn").each(function(index, ele) {
            var link = $(ele).attr("href");
            if (pathAndSearch == link) {
                $(ele).addClass("active");
                hasActive = true;
            }

            count += 1;
        });

        if (count > 0 && !hasActive) {
            $(".x-tab-default").addClass("active");
        }
    }

    function initTabBox() {
        $(".x-tab-box").each(function (index, ele) {
            var key = $(ele).attr("data-tab-key");
            var defaultValue = $(ele).attr("data-tab-default");
            var value = getUrlParam(key);
            if ( xnote.isEmpty(value) ) {
                value = defaultValue;
            }

            // 样式通过CSS控制即可
            console.log("tab-value=",value);
            var qValue = '"' + value + '"'; // 加引号quote

            $(ele).find(".x-tab[data-tab-value=" + qValue + "]").addClass("active");
            $(ele).find(".x-tab-btn[data-tab-value=" + qValue + "]").addClass("active");

            $(ele).find(".x-tab").each(function (index, child) {
                var oldHref = $(child).attr("href");
                if ( xnote.isNotEmpty(oldHref) ) {
                    return;
                }
                var tabValue = $(child).attr("data-tab-value");
                $(child).attr("href", xnote.addUrlParam(window.location.href, key, tabValue))
            })
        });
    }


    function initTabDefault() {
        // initTabLink();
        initTabBtn();
        initTabBox();
    }

    initTabDefault();
    xnote.addEventListener("init-default-value", initTabDefault);
});

// 根据内容自动调整高度
$.fn.autoHeight = function(){    
    function autoHeight(elem){
        elem.style.height = 'auto';
        elem.scrollTop = 0; //防抖动
        elem.style.height = elem.scrollHeight + 'px';
    };

    this.each(function(){
        autoHeight(this);
        $(this).on('keyup', function(){
            autoHeight(this);
        });
    });
};

// 在滚动条中展示
$.fn.showInScroll = function(offsetY) {
    if (offsetY === undefined) {
        offsetY = 0;
    }

    var parent = this.parent();
    var topDiff = this.offset().top - parent.offset().top + offsetY;
    parent.scrollTop(topDiff);
};

/**
 * 模板渲染器
 * @author xupingmao
 * @since 2021/05/01 14:56:59
 * @modified 2022/01/09 16:42:27
 * @filename x-template.js
 */


/**
 * 简单的模板渲染，这里假设传进来的参数已经进行了html转义
 * <code>
 *   var text = xnote.renderTemplate("Hello,${name}!", {name: "World"});
 *   // text = "Hello,World";
 * </code>
 */
xnote.renderTemplate = function(templateText, object) {
    function escapeHTML(text) {
        var temp = document.createElement("div");
        temp.innerHTML = text;
        return temp.innerText || temp.textContent
    }

    // TODO 处理转义问题
    // 使用 art-template
    return templateText.replace(/\$\{(.+?)\}/g, function (context, objKey) {
        var value = object[objKey.trim()] || '';
        return escapeHTML(value);
    });
};

(function() {
    function jqRenderTemplate(data, options) {
        var templateText = $(this).text();
        // 使用art-template模板渲染
        return template.render(templateText, data, options);
    }

    /**
     * 获取表单数据
     */
    $.fn.extend({
        /** 渲染模板 **/
        "render": jqRenderTemplate,
        "renderTemplate": jqRenderTemplate,
    });
})();

/**
 * 解析URL参数
 * @param {string} src 输入的URL
 * @param {boolean} doDecode 是否进行decode操作
 * @returns {object} 解析之后的对象
 */
xnote.parseUrl = function(src, doDecode) {
    // URL的完整格式如下
    // 协议://用户名:密码@子域名.域名.顶级域名:端口号/目录/文件名.文件后缀?参数=值#标志
    var path = '';
    var args = {};
    // 0: path状态; 1: argName状态; 2: argValue状态;
    var state = 0;
    var name = '';
    var value = '';

    // 默认不进行decode（兼容原来的逻辑）
    if (doDecode === undefined) {
        doDecode = false;
    }

    for(var i = 0; i < src.length; i++) {
        var c = src[i]

        // 状态判断
        if (c == '?' || c == '&') {
            state = 1; // arg name;
            if (name != '') {
                args[name] = value; 
            }
            name = '';
            continue;
        } else if (c == '=') { // arg value
            state = 2; 
            value = '';
            continue;
        }

        // 状态处理
        if (state == 0) {
            path += c; // path state
        } else if (state == 1) {
            name += c; // arg name;
        } else if (state == 2) {
            value += c;
        }
    }

    function formatValue(value) {
        if (doDecode) {
            return decodeURIComponent(value);
        } else {
            return value;
        }
    }

    if (name != '') {
        args[name] = formatValue(value);
    }
    return {'path': path, 'param': args};
}



/**
 * 获取请求参数
 */
xnote.getUrlParams = function() {
    var params = {};
    var url = window.location.href;
    url = url.split("#")[0];
    var idx = url.indexOf("?");
    if(idx > 0) {
        var queryStr = url.substring(idx + 1);
        var args = queryStr.split("&");
        for(var i = 0, a, nv; a = args[i]; i++) {
            nv = args[i] = a.split("=");
            if (nv.length > 1) {
                var value = nv[1];
                try {
                    params[nv[0]] = decodeURIComponent(value);
                } catch (e) {
                    params[nv[0]] = value;
                    console.warn('decode error', e)
                }
            }
        }
    }
    return params;
};

/**
 * 根据key获取url参数值 
 * @param {string} key
 * @param {string} defaultValue 默认值
 */
xnote.getUrlParam = function (key, defaultValue) {
    var paramValue = xnote.getUrlParams()[key];
    if (paramValue === undefined) {
        return defaultValue;
    } else {
        return paramValue;
    }
}

/**
 * 给指定的url添加参数
 * @param {string} url 指定的url
 * @param {string} key 参数的key
 * @param {string} value 参数的value
 */
xnote.addUrlParam = function(url, key, value) {
    var parsed = parseUrl(url);
    var result = parsed.path;
    var params = parsed.param;
    var isFirst = true;
    
    params[key] = encodeURIComponent(value);
    // 组装新的url
    for (var key in params) {
        var paramValue = params[key];
        if (isFirst) {
            result += "?" + key + "=" + paramValue;
            isFirst = false;
        } else {
            result += "&" + key + "=" + paramValue;
        }
    }
    return result;
}

/**
 * HTML转义
 * @param {string} text 待转义的文本
 * @returns {string}
 */
xnote.escapeHTML = function (text) {
    return $("<div>").text(text).html();
}

window.parseUrl = xnote.parseUrl
window.getUrlParam = xnote.getUrlParam
window.getUrlParams = xnote.getUrlParams
window.addUrlParam = xnote.addUrlParam
/**
* 通用的操作函数
*/
$(function () {
  
  window.moveTo = function (selfId, parentId) {
    $.post("/note/move",
    { id: selfId, parent_id: parentId },
    function (resp) {
      console.log(resp);
      window.location.reload();
    });
  }
  
  function showSideBar() {
    $(".navMenubox").animate({ "margin-left": "0px" });
    $("#poweredBy").show();
  }
  
  function hideSideBar() {
    $(".navMenubox").animate({ "margin-left": "-200px" });
    $("#poweredBy").hide();
  }
  
  function checkResize() {
    if ($(".navMenubox").is(":animated")) {
      return;
    }
    if (window.innerWidth < 600) {
      // 移动端，兼容下不支持@media的浏览器 
      hideSideBar();
    } else {
      showSideBar();
    }
  }
  
  function toggleMenu() {
    var marginLeft = $(".navMenubox").css("margin-left");
    if (marginLeft == "0px") {
      hideSideBar();
    } else {
      showSideBar();
    }
  }
  
  $(".toggleMenu").on("click", function () {
    toggleMenu();
  });
});

/**
* 处理悬浮控件
*/
$(function () {
  var width = 960;
  var maxWidth = $(window).width();
  var maxHeight = $(window).height();
  var leftPartWidth = 200;
  
  var btnRight = (maxWidth - width) / 2 + 20;
  if (btnRight < 0) {
    btnRight = 20;
  }
  var botHeight = "100%";
  var botWidth = maxWidth / 2;
  
  var bots = {};
  
  function createIframe(src) {
    return $("<iframe>")
    .addClass("dialog-iframe")
    .attr("src", src)
    .attr("id", "botIframe");
  }
  
  function createCloseBtn() {
    return $("<span>").text("Close").addClass("dialog-close-btn");
  }
  
  function createTitle() {
    var btn1 = $("<span>").text("Home").addClass("dialog-title-btn dialog-home-btn");
    var btn2 = $("<span>").text("Tools").addClass("dialog-title-btn dialog-tools-btn");
    var btn3 = $("<span>").text("Refresh").addClass("dialog-title-btn dialog-refresh-btn");
    
    return $("<div>").addClass("dialog-title")
    .append(createCloseBtn())
    .append(btn1).append(btn2).append(btn3);
  }
  
  function getBottomBot() {
    if (bots.bottom) {
      return bots.bottom;
    }
    var bot = $("<div>").css({
      "position": "fixed",
      "width": "100%",
      "height": "80%",
      "background-color": "#fff",
      "border": "1px solid #ccc",
      "bottom": "0px",
      "right": "0px",
      "z-index": 50
    }).append(createIframe("/"));
    bot.hide();
    bot.attr("id", "x-bot");
    $(document.body).append(bot);
    bots.bottom = bot;
    return bot;
  }
  
  function getIframeDialog() {
    if (bots.dialog) {
      return bots.dialog;
    }
    var mainWidth = $(".root").width();
    var bot = $("<div>").css({
      "position": "fixed",
      "width": mainWidth,
      "height": "80%",
      "background-color": "#fff",
      "border": "1px solid #ccc",
      "bottom": "0px",
      "right": "0px",
      "z-index": 50
    }).append(createIframe("/"));
    bot.hide();
    $(document.body).append(bot);
    bots.dialog = bot;
    return bot;
  }
  
  function initEventHandlers() {
    // close button event
    console.log("init");
    $("body").on("click", ".dialog-close-btn", function () {
      getRightBot().fadeOut(200);
    });
    $("body").on("click", ".dialog-home-btn", function () {
      $(".right-bot iframe").attr("src", "/");
    });
    $("body").on("click", ".dialog-tools-btn", function () {
      $(".right-bot iframe").attr("src", "/fs_api/plugins");
    });
    $("body").on("click", ".dialog-refresh-btn", function () {
      $(".right-bot iframe")[0].contentWindow.location.reload();
    });
    $("body").on("click", ".layer-btn", function (event) {
      console.log("click");
      var target = event.target;
      var url = $(target).attr("data-url");
      openDialog(url);
    });
    console.log("init done");
  }
  
  function getRightBot() {
    if (bots.right) {
      return bots.right;
    }
    var width = "50%";
    if (maxWidth < 600) {
      width = "100%";
    }
    var rightBot = $("<div>").css({
      "position": "fixed",
      "width": width,
      "right": "0px",
      "bottom": "0px",
      "top": "0px",
      "background-color": "#fff",
      "border": "solid 1px #ccc",
      "z-index": 50,
    }).append(createTitle())
    .append(createIframe("/system/index"))
    .addClass("right-bot");
    rightBot.hide();
    $(document.body).append(rightBot);
    bots.right = rightBot;
    return rightBot;
  }
  
  function initSearchBoxWidth() {
    if (window.SHOW_ASIDE == "False") {
      $(".nav-left-search").css("width", "100%");
    }
  }
  
  function init() {
    // var botBtn = $("<div>").text("工具").css("right", btnRight).addClass("bot-btn");
    // $(document.body).append(botBtn);
    $(".bot-btn").click(function () {
      getRightBot().fadeToggle(200);
    });
    initSearchBoxWidth();
    initEventHandlers();
  }
  
  function showIframeDialog(src) {
    getRightBot().fadeIn(200);
    $("#botIframe").attr("src", src);
  }
  
  function hideIframeDialog() {
    getRightBot().fadeOut(200);
  }
  
  window.openDialog = function (url) {
    var width = $(".root").width() - 40;
    var area;
    
    if (isMobile()) {
      area = ['100%', '100%'];
    } else {
      area = [width + 'px', '80%'];
    }
    
    layer.open({
      type: 2,
      shadeClose: true,
      title: '子页面',
      maxmin: true,
      area: area,
      content: url,
      scrollbar: false
    });
  }
  
  window.showIframeDialog = showIframeDialog;
  window.hideIframeDialog = hideIframeDialog;
  
  window.toggleMenu = function () {
    $(".aside-background").toggle();
    $(".aside").toggle(500);
  }
  
  /**
  * 调整高度，通过
  * @param {string} selector 选择器
  * @param {number} bottom 距离窗口底部的距离
  */
  window.adjustHeight = function (selector, bottom, options) {
    bottom = bottom || 0;
    var height = getWindowHeight() - $(selector).offset().top - bottom;
    $(selector).css("height", height).css("overflow", "auto");
    
    if (options != undefined) {
      if (options.overflow) {
        $(selector).css("overflow", options.overflow);
      }
    }
    
    return height;
  }
  
  /**
  * 调整导航栏，如果在iframe中，则不显示菜单
  */
  window.adjustNav = function () {
    if (self != top) {
      $(".nav").hide();
      $(".root").css("padding", "10px");
    }
  }
  
  window.adjustTable = function () {
    $("table").each(function (index, element) {
      var count = $(element).find("th").length;
      if (count > 0) {
        $(element).find("th").css("width", 100 / count + '%');
      }
    });
  }
  
  $(".aside-background").on('click', function () {
    toggleMenu();
  });
  
  
  if (window.PAGE_OPEN == "dialog") {
    // 使用对话框浏览笔记
    $(".dialog-link").click(function (e) {
      e.preventDefault();
      var url = $(this).attr("href");
      var width = $(".root").width();
      layer.open({
        type: 2,
        title: "查看",
        shadeClose: true,
        shade: 0.8,
        area: [width + "px", "90%"],
        scrollbar: false,
        content: url
      });
    });
  }
  
  function processInIframe() {
    
  }
  
  if (self != top) {
    processInIframe();
  }
  
  init();
});


xnote.events.fireUploadEvent = function (event) {
  xnote.fire("fs.upload", event);
};

xnote.events.onUploadEvent = function (listener) {
  xnote.on("fs.upload", listener);
};


xnote.events.fireUploadPrepareEvent = function (event) {
  console.log("fireUploadPrepareEvent", event);
  xnote.fire("fs.upload.prepare", event);
};

xnote.events.onUploadPrepareEvent = function (listener) {
  xnote.on("fs.upload.prepare", listener);
};
/**
 * 更新笔记的类目
 * @deprecated 已废弃
 * @param {object} req 更新请求
 */
xnote.updateNoteCategory = function (req) {
    if (req === undefined) {
        throw new Error("req is undefined");
    }
    if (req.noteId === undefined) {
        throw new Error("req.noteId is undefined");
    }
    if (req.value === undefined) {
        throw new Error("req.value is undefined");
    }

    var params = {
        id: req.noteId,
        key: "category",
        value: req.value
    };

    xnote.http.post("/note/attribute/update", params, function (resp) {
        console.log("update category", resp);
        if (resp.code == "success") {
            xnote.toast("更新类目成功");
            if (req.doRefresh) {
                window.location.reload();
            }
        } else {
            xnote.alert(resp.message);
        }
    });
};

/**
 * 更新类目的名称
 * @param {object} req 请求对象
 */
xnote.updateCategoryName = function (req) {
    if (req === undefined) {
        throw new Error("req is undefined");
    }
    if (req.oldName === undefined) {
        throw new Error("req.oldName is undefined");
    }
    if (req.code === undefined) {
        throw new Error("req.code is undefined");
    }

    xnote.prompt("重命名类目", req.oldName, function (newName) {
        var params = {
            code: req.code,
            name: newName
        };

        xnote.http.post("/api/note/category/update", params, function (resp) {
            if (resp.code == "success") {
                window.location.reload();
            } else {
                xnote.alert(resp.message);
            }
        });
    });
};

// 创建笔记接口
xnote.api["note.create"] = function (req) {
    xnote.validate.notUndefined(req.name, "req.name is undefined");
    xnote.validate.notUndefined(req.parentId, "req.parentId is undefined");
    xnote.validate.notUndefined(req.type, "req.type is undefined");
    xnote.validate.isFunction(req.callback, "req.callback is not function");

    var createOption = {};
    createOption.name = req.name;
    createOption.parent_id = req.parentId;
    createOption.type = req.type;
    createOption._format = "json";

    var title = req.name;

    xnote.http.post("/note/create", createOption, function (resp) {
        if (resp.code == "success") {
            req.callback(resp);
        } else {
            xnote.alert(title + "失败:" + resp.message);
        }
    });
};

// 复制笔记接口
xnote.api["note.copy"] = function (req) {
    xnote.validate.notUndefined(req.name, "req.name is undefined");
    xnote.validate.notUndefined(req.originId, "req.originId is undefined");
    var copyOption = {
        name: req.name,
        origin_id: req.originId
    };
    var title = req.name;

    xnote.http.post("/note/copy", copyOption, function (resp) {
        if (resp.code == "success") {
            req.callback(resp);
        } else {
            xnote.alert(title + "失败:" + resp.message);
        }
    });
};

var noteAPI = {};
xnote.api.note = noteAPI;


// 绑定标签
noteAPI.bindTag = function (cmd) {
    var currentTags = cmd.currentTags;
    var tagList = cmd.tagList;
    var allTagList = cmd.allTagList; // 全部的标签
    var targetId = cmd.targetId;

    if (cmd.tagType != "group" && cmd.tagType != "note") {
        throw new TypeError("无效的tagType");
    }

    // 渲染绑定标签的html
    var html = $("#bindTagTemplate").render({
        tagList: tagList,
        allTagList: allTagList,
        selectedNames: currentTags,
        manageLink: cmd.manageLink,
        globalTagList: [
            { tag_name: "待办", tag_code: "$todo$" }
        ],
    });

    console.log("bind-tag-dialog", html);

    xnote.openDialog("添加标签", html, ["确定", "取消"], function () {
        var selectedNames = [];
        $(".tag.bind.active").each(function (idx, ele) {
            var tagName = $(ele).attr("data-code");
            selectedNames.push(tagName);
        });

        var bindParams = {
            tag_type: cmd.tagType,
            group_id: cmd.groupId,
            note_id: cmd.noteId,
            tag_names: JSON.stringify(selectedNames),
        };

        xnote.http.post("/note/tag/bind", bindParams, function (resp) {
            if (resp.code != "success") {
                xnote.alert(resp.message);
            } else {
                xnote.toast("添加标签成功");
            }
            location.reload();
        });
    });
};


var NoteView = {};
xnote.action.note = NoteView;
xnote.note = NoteView;

NoteView.onTagClick = function (target) {
    $(target).toggleClass("active");
}

// 编辑笔记的标签
NoteView.editNoteTag = function (target) {
    var parentId = $(target).attr("data-parent-id");
    var noteId = $(target).attr("data-id");
    var tagsJson = $(target).attr("data-tags");
    var tagType = $(target).attr("data-tag-type");
    if (xnote.isEmpty(tagType)) {
        tagType = "note";
    }

    var listParams = {
        tag_type: tagType,
        group_id: parentId,
        v: 2,
    };

    xnote.http.get("/note/tag/list", listParams, function (resp) {
        var cmd = {
            tagType: "note", // 绑定类型始终是note
            currentTags: JSON.parse(tagsJson),
            noteId: noteId,
            manageLink: "/note/manage?parent_id=" + parentId,
        };
        // 推荐的标签
        cmd.tagList = resp.data.suggest_list;
        // 全部的标签
        cmd.allTagList = resp.data.all_list;
        // 调用绑定标签组件
        noteAPI.bindTag(cmd);
    })
};

NoteView.searchNote = function () {
    var self = this;
    var searchText = $("#note-search-text").val();
    var api = "";
    if (searchText == "") {
        api = "/note/api/timeline?type=all&limit=100";
    } else {
        api = "/note/api/timeline?type=search&key=" + searchText;
    }
    xnote.http.get(api, function (resp) {
        if (resp.code != "success") {
            xnote.toast(resp.message);
        } else {
            var templateText = self.getSelectNoteItemListTemplate();
            var html = template.render(templateText, {
                itemList: resp.data
            });
            $(".note-search-dialog-body").html(html);
        }
    });
};

NoteView.getSelectNoteItemListTemplate = function () {
    var text = "";
    text += "{{if itemList.length == 0 }}";
    text += "    <p class=\"align-center\">空空如也~</p>";
    text += "{{/if}}";
    text += "{{each itemList item}}";
    text += "<h3 class=\"card-title-2\">{{item.title}}</h3>";
    text += "    {{each item.children subItem }}";
    text += "    <p class=\"card-row share-dialog-row\">";
    text += "        <i class=\"fa {{subItem.icon}}\"></i>";
    text += "        <a href=\"{{subItem.url}}\">{{subItem.name}}</a>";
    text += "        <input type=\"checkbox\"";
    text += "            class=\"select-note-checkbox float-right\" ";
    text += "            data-id=\"{{subItem.id}}\">";
    text += "    <p>";
    text += "    {{/each}}";
    text += "{{/each}}";
    return text;
}

NoteView.getSelectNoteDialogTemplate = function () {
    var text = "";
    text += "<div class=\"card\">";
    text += "<div class=\"row\">";
    text += "    <input type=\"text\" class=\"nav-search-input\" id=\"note-search-text\" placeholder=\"搜索笔记\" ";
    text += "        value=\"{{searchText}}\" onkeyup=\"xnote.action.note.searchNote(this);\">";
    text += "    <button class=\"nav-search-btn btn-default\" onclick=\"xnote.action.note.searchNote(this)\">";
    text += "        <i class=\"fa fa-search\"></i>";
    text += "    </button>";
    text += "</div>";
    text += "<div class=\"row note-search-dialog-body\" style=\"padding-top: 10px;\">";
    text += this.getSelectNoteItemListTemplate();
    text += "</div>";
    text += "</div>";
    return text;
};


NoteView.renderNoteList = function (itemList) {
    var templateText = this.getSelectNoteDialogTemplate();
    var html = template.render(templateText, {
        itemList: itemList
    });
    return html;
};

NoteView.openDialogToAddNote = function (event) {
    var tagCode = $(event.target).attr("data-code");
    xnote.http.get("/note/api/timeline?type=all&limit=100", function (resp) {
        if (resp.code != "success") {
            xnote.alert(resp.message);
        } else {
            var html = NoteView.renderNoteList(resp.data);
            xnote.openDialog("选择笔记", html, ["确定", "取消"], function () {
                NoteView.addNoteToTag(tagCode);
            });
        }
    });
};

NoteView.addNoteToTag = function (tagCode) {
    var selectedIds = [];
    $(".select-note-checkbox:checked").each(function (idx, ele) {
        var noteId = $(ele).attr("data-id");
        selectedIds.push(noteId);
    });
    console.log(selectedIds);

    var params = {
        action: "add_note_to_tag",
        tag_code: tagCode,
        note_ids: selectedIds.join(",")
    };
    xnote.http.post("/note/tag/bind", params, function (resp) {
        if (resp.code != "success") {
            xnote.alert(resp.message);
        } else {
            xnote.toast("添加成功");
            location.reload();
        }
    });
};

// 选择笔记本-平铺视图
// 这个函数需要配合group_select_script.html使用
NoteView.selectGroupFlat = function (req) {
    var noteId = req.noteId;
    var respData;

    xnote.validate.isFunction(req.callback, "参数callback无效");

    function bindEvent() {
        $(".group-select-box").on("keyup", ".nav-search-input", function (event) {
            /* Act on the event */
            // console.log("event", event);
            var searchKey = $(this).val().toLowerCase();

            var newData = [];

            for (var i = 0; i < respData.length; i++) {
                var item = respData[i];
                if (item.name.toLowerCase().indexOf(searchKey) >= 0) {
                    newData.push(item);
                }
            }
            renderData(newData);
        });

        $(".group-select-box").on("click", ".link", function (event) {
            var dataId = $(event.target).attr("data-id");
            req.callback(dataId);
        });
    }

    function Section() {
        this.children = [];
        this.title = "title";
    }

    Section.prototype.add = function (item) {
        this.children.push(item);
    }

    Section.prototype.isVisible = function () {
        return this.children.length > 0;
    }

    // 渲染数据
    function renderData(data) {
        var first = new Section();
        var second = new Section();
        var last = new Section();
        var firstGroup = new Section(); // 一级笔记本
        for (var i = 0; i < data.length; i++) {
            var item = data[i];
            if (item.level >= 1) {
                first.add(item);
            } else if (item.level < 0) {
                last.add(item);
            } else if (item.parent_id == 0) {
                firstGroup.add(item);
            } else {
                second.add(item);
            }
        }

        first.title = "置顶";
        firstGroup.title = "一级笔记本";
        second.title = "其他笔记本";
        last.title = "归档";

        var groups = [first, firstGroup, second, last];
        var hasNoMatch = (data.length === 0);

        var html = $("#group_select_tpl").renderTemplate({
            groups: groups,
            noteId: noteId,
            hasNoMatch: hasNoMatch
        });
        $(".group-select-data").html(html);
    }

    xnote.http.get("/note/api/group?list_type=all&orderby=name", function (resp) {
        if (resp.code != "success") {
            xnote.alert(resp.message);
            return;
        }

        respData = resp.data;
        xnote.showDialog("移动笔记", $(".group-select-box"));
        // 绑定事件
        bindEvent();
        // 渲染数据
        renderData(respData);
    });
};

// 选择笔记本-树视图
NoteView.selectGroupTree = function () {
    // 树视图目前用的是html-ajax接口   
}

// 删除标签元信息
NoteView.deleteTagMeta = function (tagMetaList) {
    var html = $("#deleteTagTemplate").render({
        tagList: tagMetaList,
    });

    xnote.openDialog("删除标签", html, ["确定删除", "取消"], function () {
        var tagIds = [];
        $(".tag.delete.active").each(function (idx, ele) {
            var tagId = $(ele).attr("data-id");
            tagIds.push(tagId);
        });

        var deleteParams = {
            tag_type: "group",
            tag_ids: JSON.stringify(tagIds),
        };
        xnote.http.post("/note/tag/delete", deleteParams, function (resp) {
            if (resp.code != "success") {
                xnote.alert(resp.message);
            } else {
                xnote.toast("删除成功,准备刷新...");
                setTimeout(function () {
                    window.location.reload()
                }, 500);
            }
            refreshTagTop();
        });
    });
};

// 打开对话框移动笔记
NoteView.openDialogToMove = function (note_id) {
    var req = {};
    req.callback = function (parentId) {
        if (parentId === undefined || parentId == "") {
            xnote.alert("parentId is undefined");
            return;
        }
        xnote.http.post("/note/move", { id: note_id, parent_id: parentId }, function (resp) {
            console.log(resp);
            window.location.reload();
        });
    };
    this.selectGroupFlat(req);
};

// 打开对话框移动笔记
NoteView.openDialogToMoveByElement = function (target) {
    return this.openDialogToMove($(target).attr("data-id"));
}


// 点击标签操作
NoteView.onTagClick = function (target) {
    $(target).toggleClass("active");
}

// 打开对话框进行分享
NoteView.openDialogToShare = function (target) {
    var id = $(target).attr("data-id");
    var type = $(target).attr("data-note-type");
    var params = {note_id: id};
    var ajax_dialog_url   = "/note/ajax/share_group_dialog";
    var ajax_dialog_title = "分享笔记本";

    if (type != "group") {
        ajax_dialog_url = "/note/ajax/share_note_dialog";
        ajax_dialog_title = "分享笔记";
    }

    xnote.http.get(ajax_dialog_url, params, function (resp) {
        xnote.showDialog(ajax_dialog_title, resp);
    });
}

// 修改排序
NoteView.changeOrderBy = function (target) {
    var id = $(target).attr("data-id");
    var orderby = $(target).val();

    checkNotEmpty(id, "data-id为空");
    checkNotEmpty(orderby, "data-orderby为空");

    xnote.http.post("/note/orderby", {id: id, orderby: orderby}, function (resp) {
        var code = resp.code;
        if (code != "success") {
            xnote.alert(resp.message);
        } else {
            xnote.toast(resp.message);
            window.location.reload();
        }
    })
};

// 修改笔记的等级（置顶之类的）
NoteView.changeLevel = function (target) {
    var id = $(target).attr("data-id");
    var status = $(target).val();

    checkNotEmpty(id, "data-id为空");
    checkNotEmpty(status, "data-status为空");

    xnote.http.post("/note/status", {id: id, status: status}, function (resp) {
        var code = resp.code;
        if (code != "success") {
            xnote.alert(resp.message);
        } else {
            xnote.toast(resp.message);
            window.location.reload();
        }
    });
}/**
 * 文件相关函数
 */
var FileView = {};
var FileAPI = {};

xnote.action.fs = FileView;
xnote.api.fs = FileAPI;


// 调用重命名的API
FileAPI.rename = function(dirname, oldName, newName, callback) {
    if (newName != oldName && newName) {
        xnote.http.post("/fs_api/rename", 
            {dirname: dirname, old_name: oldName, new_name: newName}, 
            function (resp) {
                if (resp.code == "success") {
                    callback(resp);
                } else {
                    xnote.alert("重命名失败:" + resp.message);
                }
        });
    } else {
        xnote.alert("请输入有效文件名");
    }
};


// 删除文件
FileView.delete = function(target) {
    var path = $(target).attr("data-path");
    var name = $(target).attr("data-name");
        
    xnote.confirm("确定删除【" + name + "】?", function (value) {
        xnote.http.post("/fs_api/remove", {path: path}, function (resp) {
            if (resp.code == "success") {
                window.location.reload();
            } else {
                xnote.alert("删除失败:" + resp.message);
            }
        });
    });
};

// 重命名
FileView.rename = function(target) {
    var filePath = $(target).attr("data-path");
    var oldName = $(target).attr("data-name");
    var realname = $(target).attr("data-realname");
    if (xnote.isEmpty(realname)) {
        realname = oldName;
    }

    var dirname = $("#currentDir").val();
    xnote.prompt("输入新的文件名", oldName, function (newName) {
        FileAPI.rename(dirname, realname, newName, function(resp) {
            window.location.reload();
        });
    });
};

// 打开选项对话框
FileView.openOptionDialog = function (target) {
    console.log(window.event);
    window.event.preventDefault();
    window.event.stopPropagation();
    console.log(target);
    var filePath = $(target).attr("data-path");
    var fileName = $(target).attr("data-name");
    var fileRealName = $(target).attr("data-realname");
    var html = $("#fileItemOptionDialog").render({
        "filePath": filePath,
        "fileName": fileName,
        "fileRealName": fileRealName
    });

    xnote.openDialog("选项", html);
};
