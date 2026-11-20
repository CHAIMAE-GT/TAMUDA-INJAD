/* Carrousel de témoignages — généré par build.py */
(function(){
  function init(root){
    var track=root.querySelector(".t-track"),slides=[].slice.call(track.children),
        dotsBox=root.querySelector(".t-dots"),prev=root.querySelector(".t-prev"),next=root.querySelector(".t-next"),
        pause=root.querySelector(".t-pause"),count=root.querySelector(".t-count"),
        reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches,
        playing=!reduce,hover=false,timer=null,page=0;
    function per(){return Math.max(1,Math.round(track.clientWidth/slides[0].offsetWidth));}
    function pages(){return Math.ceil(slides.length/per());}
    function step(){return slides.length>1?slides[1].offsetLeft-slides[0].offsetLeft:track.clientWidth;}
    function drawDots(){
      dotsBox.innerHTML="";
      for(var i=0;i<pages();i++){(function(i){
        var b=document.createElement("button");b.type="button";b.className="t-dot";
        b.setAttribute("aria-label","Groupe "+(i+1)+" sur "+pages());
        b.addEventListener("click",function(){go(i,true);});dotsBox.appendChild(b);})(i);}
      root.classList.toggle("is-static",pages()<2);mark();
    }
    function mark(){
      [].forEach.call(dotsBox.children,function(d,i){i===page?d.setAttribute("aria-current","true"):d.removeAttribute("aria-current");});
      var a=page*per()+1,z=Math.min(slides.length,a+per()-1);
      count.textContent="Témoignages "+a+(z>a?" à "+z:"")+" sur "+slides.length;
    }
    function go(p,user){
      var n=pages();page=(p+n)%n;
      track.scrollTo({left:page*per()*step(),behavior:reduce?"auto":"smooth"});mark();
      if(user)restart();
    }
    var tick;track.addEventListener("scroll",function(){
      clearTimeout(tick);tick=setTimeout(function(){
        var p=Math.round(track.scrollLeft/(per()*step()));
        if(track.scrollLeft+track.clientWidth>=track.scrollWidth-2)p=pages()-1;
        if(p!==page){page=Math.max(0,Math.min(pages()-1,p));mark();}},90);},{passive:true});
    function stop(){clearInterval(timer);timer=null;}
    function restart(){stop();if(playing&&!hover&&!document.hidden&&pages()>1)timer=setInterval(function(){go(page+1);},6500);}
    prev.addEventListener("click",function(){go(page-1,true);});
    next.addEventListener("click",function(){go(page+1,true);});
    pause.addEventListener("click",function(){
      playing=!playing;pause.setAttribute("aria-pressed",String(!playing));
      pause.textContent=playing?"❚❚":"▶";
      pause.setAttribute("aria-label",playing?"Mettre en pause le défilement automatique":"Reprendre le défilement automatique");restart();});
    track.addEventListener("keydown",function(e){
      if(e.key==="ArrowRight"){e.preventDefault();go(page+1,true);}
      if(e.key==="ArrowLeft"){e.preventDefault();go(page-1,true);}});
    ["mouseenter","focusin","touchstart"].forEach(function(ev){root.addEventListener(ev,function(){hover=true;stop();},{passive:true});});
    ["mouseleave","focusout"].forEach(function(ev){root.addEventListener(ev,function(){hover=false;restart();});});
    document.addEventListener("visibilitychange",restart);
    window.addEventListener("resize",function(){drawDots();go(Math.min(page,pages()-1));});
    if(reduce){pause.setAttribute("aria-pressed","true");pause.textContent="▶";
      pause.setAttribute("aria-label","Activer le défilement automatique");}
    drawDots();restart();
  }
  function ready(){[].forEach.call(document.querySelectorAll("[data-carousel]"),init);}
  document.readyState==="loading"?document.addEventListener("DOMContentLoaded",ready):ready();
})();
