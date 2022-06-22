window.onload = function (){

    // timer start

    // let time = 0;
    // let hour = 0;
    // let min = 0;
    // let sec = 0;
    // let timer;
    //
    // const countUp = () => {
    //     timer = setInterval(()=>{
    //         time ++;
    //         min = Math.floor(time/60);
    //         hour = Math.floor(min/60);
    //         sec = time%60;
    //         min = min%60;
    //
    //         let th = hour;
    //         let tm = min;
    //         let ts = sec;
    //         if (th<10){
    //             th = `0${hour}`
    //         }
    //         if (tm<10){
    //             tm = `0${min}`
    //         }
    //         if (ts<10){
    //             ts = `0${sec}`
    //         }
    //         document.querySelector('.timer').innerHTML = `${th}:${tm}:${ts}`;
    //     },1000);
    // }
    // countUp();

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

    // input value 가져오기
    // const quizAnswer = document.querySelector('.quiz-input');
    // quizAnswer.addEventListener('keypress',(e)=>{
    //     if(e.key === 'Enter'){
    //         let quizValue = quizAnswer.value;
    //         console.log(quizValue);
    //         quizAnswer.value = '';
    //     }
    // });


    // timer end

}