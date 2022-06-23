window.onload = function (){


    let downtime = 60;
    const countDown = () => {
        setInterval(()=>{
            downtime --;
            if(downtime <= 0){
                document.querySelector('.quiz-modal').style.display = 'flex';
                downtime = 0;
            }
            if(downtime < 10){
                document.querySelector('.timer').innerHTML = `00:0${downtime}`
            }else{
                document.querySelector('.timer').innerHTML = `00:${downtime}`
            }
        },1000);
    }
    countDown();
}