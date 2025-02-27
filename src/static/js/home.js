const xps = document.getElementsByClassName('xp');
const totalXP = document.getElementById('total-xp');

function getXP() {
    let xpVal = 0;
    for(let i =0; i < xps.length; i++) {
        xpVal += parseInt(xps[i].innerHTML);
    }
    return xpVal;
}

function setXP() {
    totalXP.innerHTML += getXP();
}

setXP();