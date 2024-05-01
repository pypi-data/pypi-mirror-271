/**
 * Minified by jsDelivr using Terser v5.17.1.
 * Original file: /npm/@simondmc/popup-js@1.4.2/popup.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
const queuedPopups=[];let loadPhase=0;const head=document.getElementsByTagName("head")[0],link=document.createElement("link");function loadPopups(){for(;queuedPopups.length>0;)queuedPopups.shift().init()}link.rel="stylesheet",link.type="text/css",link.href="https://cdn.jsdelivr.net/npm/@simondmc/popup-js@1.4.2/popup.min.css",link.media="all",head.appendChild(link),link.onload=function(){loadPhase+=1,2===loadPhase&&loadPopups()},window.addEventListener("load",(()=>{loadPhase+=1,2===loadPhase&&loadPopups()}));class Popup{constructor(t={}){this.params=t,2==loadPhase?this.init():queuedPopups.push(this)}init(){this.id=this.params.id??"popup",this.title=this.params.title??"Popup Title",this.content=this.params.content??"Popup Content",this.titleColor=this.params.titleColor??"#000000",this.backgroundColor=this.params.backgroundColor??"#ffffff",this.closeColor=this.params.closeColor??"#000000",this.textColor=this.params.textColor??"#000000",this.linkColor=this.params.linkColor??"#383838",this.widthMultiplier=this.params.widthMultiplier??1,this.heightMultiplier=this.params.heightMultiplier??.66,this.fontSizeMultiplier=this.params.fontSizeMultiplier??1,this.borderRadius=this.params.borderRadius??"15px",this.sideMargin=this.params.sideMargin??"3%",this.titleMargin=this.params.titleMargin??"2%",this.lineSpacing=this.params.lineSpacing??"auto",this.showImmediately=this.params.showImmediately??!1,this.showOnce=this.params.showOnce??!1,this.fixedHeight=this.params.fixedHeight??!1,this.allowClose=this.params.allowClose??!0,this.underlineLinks=this.params.underlineLinks??!1,this.fadeTime=this.params.fadeTime??"0.3s",this.buttonWidth=this.params.buttonWidth??"fit-content",this.borderWidth=this.params.borderWidth??"0",this.borderColor=this.params.borderColor??"#000000",this.disableScroll=this.params.disableScroll??!0,this.textShadow=this.params.textShadow??"none",this.hideCloseButton=this.params.hideCloseButton??!1,this.hideTitle=this.params.hideTitle??!1,this.height=`min(${770*this.heightMultiplier}px, ${90*this.heightMultiplier}vw)`,this.width=`min(${770*this.widthMultiplier}px, ${90*this.widthMultiplier}vw)`,this.fontSize=`min(${25*this.fontSizeMultiplier}px, ${5.5*this.fontSizeMultiplier}vw)`,this.css=this.params.css??"",this.css+=`\n        .popup.${this.id} {\n            transition-duration: ${this.fadeTime};\n            text-shadow: ${this.textShadow};\n            font-family: '${this.params.font??"Inter"}', 'Inter', Helvetica, sans-serif;\n        }\n        \n        .popup.${this.id} .popup-content {\n            background-color: ${this.backgroundColor};\n            width:${this.width}; \n            height:${this.fixedHeight?this.height:"fit-content"};\n            border-radius: ${this.borderRadius};\n            border: ${this.borderWidth} solid ${this.borderColor};\n        }\n\n        .popup.${this.id} .popup-header {\n            margin-bottom: ${this.titleMargin};\n        }\n\n        .popup.${this.id} .popup-title {\n            color: ${this.titleColor};\n        }\n\n        .popup.${this.id} .popup-close {\n            color: ${this.closeColor};\n        }\n\n        .popup.${this.id} .popup-body {\n            color: ${this.textColor};\n            margin-left: ${this.sideMargin};\n            margin-right: ${this.sideMargin};\n            line-height: ${this.lineSpacing};\n            font-size: ${this.fontSize};\n        }\n\n        .popup.${this.id} .popup-body button { \n            width: ${this.buttonWidth}; \n        }\n\n        .popup.${this.id} .popup-body a { \n            color: ${this.linkColor};\n            ${this.underlineLinks?"text-decoration: underline;":""}\n        }`;const t=document.head,i=document.createElement("style");t.append(i),i.appendChild(document.createTextNode(this.css)),this.content=this.content.split("\n");for(let t=0;t<this.content.length;t++){let i=this.content[t].trim();if(""!==i){if(i.includes("§")){const t=i.split("§");i=`<p class="${t[0].trim()}">${t[1].trim()}</p>`}else i=`<p>${i}</p>`;for(i=i.replace(/  /g,"&nbsp;&nbsp;");/{a-(.*?)}\[(.*?)]/.test(i);)i=i.replace(/{a-(.*?)}\[(.*?)]/g,'<a href="$1" target="_blank">$2</a>');for(;/{btn-(.*?)}\[(.*?)]/.test(i);)i=i.replace(/{btn-(.*?)}\[(.*?)]/g,'<button class="$1">$2</button>');i=i.replace(/([^\\]?){/g,'$1<span class="').replace(/([^\\]?)}\[/g,'$1">').replace(/([^\\]?)]/g,"$1</span>"),this.content[t]=i}}if(this.content=this.content.join(""),this.popupEl=document.createElement("div"),this.popupEl.classList.add("popup"),this.popupEl.classList.add(this.id),this.popupEl.innerHTML=`\n        <div class="popup-content">\n            <div class="popup-header">\n                ${this.hideTitle?"":`<div class="popup-title">${this.title}</div>`}\n                ${this.allowClose&&!this.hideCloseButton?'<div class="popup-close">&times;</div>':""}\n            </div>\n            <div class="popup-body">${this.content}</div>\n        </div>`,document.body.appendChild(this.popupEl),this.popupEl.addEventListener("click",(t=>{if("popup-close"==t.target.className||t.target.classList.contains("popup")){if(!this.allowClose)return;this.hide()}})),this.params.loadCallback&&"function"==typeof this.params.loadCallback&&this.params.loadCallback(),this.showImmediately){if(this.showOnce&&localStorage&&localStorage.getItem("popup-"+this.id))return;this.popupEl.classList.add("fade-in"),postShow(disableScroll)}document.addEventListener("keydown",(t=>{if("Escape"===t.key){if(!this.allowClose)return;this.hide()}}))}show(){this.popupEl.classList.remove("fade-out"),this.popupEl.classList.add("fade-in"),postShow(this.params.disableScroll??!0)}hide(){this.popupEl.classList.remove("fade-in"),this.popupEl.classList.add("fade-out"),localStorage&&this.showOnce&&localStorage.setItem("popup-"+this.id,!0),postHide(this)}}function postShow(t){t&&disableScroll()}function postHide(t){t.params.hideCallback&&"function"==typeof t.params.hideCallback&&t.params.hideCallback(),enableScroll()}function disableScroll(){const t=window.scrollY||document.documentElement.scrollTop,i=window.scrollX||document.documentElement.scrollLeft;window.onscroll=function(){window.scrollTo(i,t)}}function enableScroll(){window.onscroll=function(){}}
//# sourceMappingURL=/sm/5ba2ebb3f807f0f3b58c5b7aa1f6be09dff888682d73a99a23b7774fec9aa2c8.map