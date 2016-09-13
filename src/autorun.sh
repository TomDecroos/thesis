function setcmd {
smallcmd='screen -dm python main.py multi dtw '$smallercmd' 10 resultsk10'
CMD='cd thesis/src ; '
CMD+=$smallcmd' '$1' '$2'; '
CMD+=$smallcmd' '$2' '$3'; '
CMD+=$smallcmd' '$3' '$4'; '
}

function loadonhimec04 {
setcmd 0 5 10 15
ssh himec04.cs.kuleuven.be $CMD
setcmd 15 20 25 30
ssh himec04.cs.kuleuven.be $CMD
setcmd 30 35 40 45
ssh himec04.cs.kuleuven.be $CMD
setcmd 45 50 55 60
ssh himec04.cs.kuleuven.be $CMD
setcmd 60 63 66 69
ssh himec04.cs.kuleuven.be $CMD
}

function loadonhimec02 {
setcmd 0 5 10 15
ssh himec02.cs.kuleuven.be $CMD
setcmd 15 20 25 30
ssh himec02.cs.kuleuven.be $CMD
setcmd 30 35 40 45
ssh himec02.cs.kuleuven.be $CMD
setcmd 45 50 55 60
ssh himec02.cs.kuleuven.be $CMD
setcmd 60 63 66 69
ssh pinac21.cs.kuleuven.be $CMD
}

function loadonpinacs1 {
setcmd 0 5 10 15
ssh pinac38.cs.kuleuven.be $CMD
setcmd 15 20 25 30
ssh pinac37.cs.kuleuven.be $CMD
setcmd 30 35 40 45
ssh pinac39.cs.kuleuven.be $CMD
setcmd 45 50 55 60
ssh pinac33.cs.kuleuven.be $CMD
setcmd 60 63 66 69
ssh pinac24.cs.kuleuven.be $CMD
}

function loadonpinacs2 {
setcmd 0 5 10 15
ssh pinac26.cs.kuleuven.be $CMD
setcmd 15 20 25 30
ssh pinac21.cs.kuleuven.be $CMD
setcmd 30 35 40 45
ssh pinac28.cs.kuleuven.be $CMD
setcmd 45 50 55 60
ssh pinac22.cs.kuleuven.be $CMD
setcmd 60 63 66 69
ssh pinac23.cs.kuleuven.be $CMD
}

smallercmd='indirect'
loadonhimec02

smallercmd='direct'
loadonhimec04

