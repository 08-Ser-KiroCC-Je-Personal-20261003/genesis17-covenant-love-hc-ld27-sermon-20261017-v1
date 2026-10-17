(function(){
  var b=document.body,root=document.documentElement;
  var th=localStorage.getItem('theme');if(th)root.setAttribute('data-theme',th);
  function $(s){return document.querySelector(s)}function $$(s){return Array.prototype.slice.call(document.querySelectorAll(s))}
  var tg=$('#tocBtn');if(tg)tg.onclick=function(){if(innerWidth<=960)b.classList.toggle('toc-open');else b.classList.toggle('toc-off')};
  $$('#toc a').forEach(function(a){a.addEventListener('click',function(){if(innerWidth<=960)b.classList.remove('toc-open')})});
  var thb=$('#themeBtn');if(thb)thb.onclick=function(){var n=root.getAttribute('data-theme')==='light'?'dark':'light';root.setAttribute('data-theme',n);localStorage.setItem('theme',n)};
  var bar=$('#bar');addEventListener('scroll',function(){var h=root.scrollHeight-innerHeight;bar.style.width=(h>0?scrollY/h*100:0)+'%'},{passive:true});
  var links={};$$('#toc a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&links[e.target.id]){$$('#toc a.on').forEach(function(x){x.classList.remove('on')});links[e.target.id].classList.add('on')}})},{rootMargin:'-20% 0px -70% 0px'});
    Object.keys(links).forEach(function(id){var el=document.getElementById(id);if(el)io.observe(el)})}
  $$('.fc').forEach(function(c){c.setAttribute('tabindex','0');c.onclick=function(){c.classList.toggle('flip')};c.onkeydown=function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();c.classList.toggle('flip')}}});
  $$('.tabs').forEach(function(t){var bs=t.querySelectorAll('.btn');Array.prototype.forEach.call(bs,function(x){x.onclick=function(){Array.prototype.forEach.call(bs,function(y){y.classList.remove('on');var p=document.getElementById(y.dataset.p);if(p)p.classList.remove('on')});x.classList.add('on');document.getElementById(x.dataset.p).classList.add('on')}})});
  var rb=$('#reciteBtn');if(rb)rb.onclick=function(){b.classList.toggle('recite');$$('.ln.show').forEach(function(x){x.classList.remove('show')});rb.textContent=b.classList.contains('recite')?'👁 显示全文':'🙈 背诵模式'};
  $$('.creed .ln').forEach(function(l){l.onclick=function(){l.classList.toggle('show')}});
  var fs=16;function setF(d){fs=Math.min(24,Math.max(14,fs+d));$$('.creed').forEach(function(c){c.style.fontSize=fs+'px'})}
  var fp=$('#fPlus'),fm=$('#fMinus');if(fp)fp.onclick=function(){setF(2)};if(fm)fm.onclick=function(){setF(-2)};
})();
