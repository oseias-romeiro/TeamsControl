let copy = (link)=>{
    navigator.clipboard.writeText(link);
    alert("link copyed!");
}
let btnLink = document.getElementById('btn-team-link');
btnLink.addEventListener('click', ()=>{
    copy(window.location.origin+btnLink.innerText);
});