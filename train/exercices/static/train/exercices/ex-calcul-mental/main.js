EXERCICE_PLAYER.register ( 'calcul-mental', function generator ( html ) {
    let calcul="";
    let nb_calcs=Math.ceil(Math.random()*10)
    for(let i=0;i<nb_calcs;i++){
        let number=Math.floor(Math.random()*20)
        calcul+=String(number)
        let operation=Math.floor(Math.random()*3)
        if(operation==0){
            calcul+="+"
        } else if(operation==1){
            calcul+="-"
        } else if(operation==2){
            calcul+="*"
        }
    }
    let number=Math.ceil(Math.random()*20)
    calcul+=number
    let ans=eval(calcul)
    return {calcul, ans}

}, function show_exercice(exercice) {
    let container=EXERCICE_PLAYER.get_exercice_container();
    container.innerHTML=`<div class="text-center p-4 mb-4">
    <div class="text-3xl flex">
        <div class="flex-1"></div>
        Calcul mental
        <div class="text-gray-400 pl-4" id="remaining-number"></div>
        <div class="flex-1"></div>
    </div>
</div>
<div class='center-w text-center mt-16 relative center-h'><p style='font-size:4rem;'>`+exercice.calcul+`</p></div>`
}, function show_solution (exercice) {
    let container = EXERCICE_PLAYER.get_exercice_container();
    EXERCICE_PLAYER.timer=0;
    container.innerHTML = "";
    container.innerHTML+=`<div class="text-center p-4 mb-4">
    <div class="text-3xl flex">
        <div class="flex-1"></div>
        Calcul mental
        <div class="text-gray-400 pl-4" id="remaining-number"></div>
        <div class="flex-1"></div>
    </div>
</div>
<div class='center-w text-center mt-16 relative'><p style='font-size:4rem;'>`+exercice.calcul+`</p><p style='font-size:4rem;'>= `+exercice.ans+`</p></div>`
} )
