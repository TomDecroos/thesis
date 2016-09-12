function setcmd {
smallcmd='screen -dm python main.py multi naive direct'
CMD='cd thesis/src; '
CMD+=$smallcmd' '$1' '$2'; '
CMD+=$smallcmd' '$2' '$3'; '
CMD+=$smallcmd' '$3' '$4'; '
}

setcmd 0 5 10 15
ssh pinac39.cs.kuleuven.be $CMD

setcmd 15 20 25 30
ssh pinac33.cs.kuleuven.be $CMD

setcmd 30 35 40 45
ssh pinac37.cs.kuleuven.be $CMD

setcmd 45 50 55 60
ssh pinac31.cs.kuleuven.be $CMD

setcmd 60 63 66 69
ssh pinac21.cs.kuleuven.be $CMD


