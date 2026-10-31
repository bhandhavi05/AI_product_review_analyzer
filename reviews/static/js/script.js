document.addEventListener("DOMContentLoaded",()=>{

    console.log("AI Product Review Analyzer Loaded");

    const cards=document.querySelectorAll(".feature-card");

    cards.forEach(card=>{
        card.addEventListener("mouseenter",()=>{
            card.style.transition="0.3s";
        });
    });

});