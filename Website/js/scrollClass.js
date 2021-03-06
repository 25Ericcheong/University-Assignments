/*!
 * scrollClass jQuery Plugin v1.1
 *
 * Author: Virgiliu Diaconu
 * http://www.virgiliu.com
 * Licensed under the MIT license.
 */
!function(o,l,t,n){"use strict";o.scrollClass=function(n,s){var i=this;i.$el=o(n),i.el=n,i.$win=o(l),i.$doc=o(t);var e,a=!1;i.init=function(){i.options=o.extend({},o.scrollClass.defaultOptions,s)},i.scrollHandler=function(){a||i.onScroll()},i.onScroll=function(){if(i.inViewport())return 0!==i.options.delay?(l.clearTimeout(e),e=l.setTimeout(i.addScrollClass,i.options.delay)):i.addScrollClass(),"function"==typeof i.options.callback&&i.options.callback.call(n),void(a=!0)},i.addScrollClass=function(){var o=i.$el.data("scrollClass");i.$el.addClass(o)},i.inViewport=function(){var o=i.el.getBoundingClientRect(),l=i.$win.height(),t=i.options.threshold;l<o.height&&(t=50);var n=t/100*o.height;return o.top+n<=l&&o.bottom-n>=0+i.options.offsetTop},i.init(),i.$win.on("scroll load",i.scrollHandler)},o.scrollClass.defaultOptions={delay:10,threshold:50,offsetTop:0},o.fn.scrollClass=function(l){return this.each(function(){new o.scrollClass(this,l)})}}(jQuery,window,document);
