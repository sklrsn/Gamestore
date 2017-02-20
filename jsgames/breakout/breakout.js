$(document).ready(function() {
    var message = {
        messageType: "SETTING",
        options: {
            "width": 360, //Integer
            "height": 600 //Integer
        }
    };


    function InitilizeGame() {
        window.parent.postMessage(message, "*");
        canvas = $("#gameCanvas");
        mCanvas = canvas[0];
        ctx = mCanvas.getContext("2d");
        mCanvas.height =600- $('.toolbar').height()-20;
        //console.log("window.innerHeight : "+window.innerHeight);
        //console.log("window.innerWidth : "+window.innerWidth);
        //Setting the width of the game canvas to maximum of 360
        if (window.innerWidth > 360)
            mCanvas.width = 360;
        else
            mCanvas.width = window.innerWidth-10;
        //console.log("main.width " +mCanvas.width);
        ballRadius = 10;
        x = mCanvas.width / 2;
        y = mCanvas.height - 30;
        //console.log("mCanvas.height - 30 : "+y)
        // speed of ball
        speed = 3;
        dx = speed;
        dy = -1 * speed;
        paddleHeight = 10;
        paddleWidth = 75;
        paddleX = (mCanvas.width - paddleWidth) / 2;
        rightPressed = false;
        leftPressed = false;
        brickRowCount = 5;
        brickColumnCount = 3;
        brickWidth = mCanvas.width / 7;
        brickHeight = mCanvas.height / 40;
        brickPadding = 10;
        brickOffsetTop = 30;
        brickOffsetLeft = 30;
        score = 0;
        lives = 3;
        level = 1;
        bricks = [];
    }
    // Initializing the bricks with status as 1 (not broken)
    function initializeBricks() {
        var maxSuperBrick = (level - 1) * 3;
        if (maxSuperBrick > 15)
            maxSuperBrick = 15;
        for (c = 0; c < brickColumnCount; c++) {
            bricks[c] = [];
            for (r = 0; r < brickRowCount; r++) {
                var superStatus = 1;
                // Setting the level of brick
                if (maxSuperBrick > 0) {
                    superStatus = Math.floor((Math.random() * 3) + 1);
                    if (superStatus > 1)
                        maxSuperBrick--;
                }

                bricks[c][r] = {
                    x: 0,
                    y: 0,
                    status: superStatus
                };
            }
        }
    }

    //captures the key movement
    $(this).keyup(function(e) {
        if (e.keyCode == 39) {
            rightPressed = false;
        } else if (e.keyCode == 37) {
            leftPressed = false;
        }
    });
    $(this).keydown(function(e) {
        if (e.keyCode == 39) {
            rightPressed = true;
        } else if (e.keyCode == 37) {
            leftPressed = true;
        }
    });
    //captures the mouse movement
    $(this).mousemove(function(e) {
        $('.another').html(e.clientX + "#" + mCanvas.offsetLeft);
        var relativeX = e.clientX - mCanvas.offsetLeft;
        if (relativeX <= paddleWidth)
            paddleX = 0;
        else if (relativeX > 0 && relativeX < mCanvas.width) {
            paddleX = relativeX - paddleWidth;
        }
    });

    // detects collision of the ball with the brick
    function collisionDetection() {
        for (c = 0; c < brickColumnCount; c++) {
            for (r = 0; r < brickRowCount; r++) {
                var b = bricks[c][r];
                if (b.status >= 1) {
                    if (x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
                        dy = -dy;
                        b.status--;
                        score++;
                        if (getBricksStatus()==0) {
                          //console.log(getBricksStatus());
                            level++;
                            speed += 1;
                            dx = speed;
                            dy = -1 * speed;
                            paddleX = (mCanvas.width - paddleWidth) / 2;
                            x = mCanvas.width / 2;
                            y = mCanvas.height - 30;
                            initializeBricks();
                            //document.location.reload();
                        }
                    }
                }
            }
        }
    }

    function drawBall() {
        ctx.beginPath();
        ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
        ctx.fillStyle = "#0095DD";
        ctx.fill();
        ctx.closePath();
    }

    function drawPaddle() {
        ctx.beginPath();
        ctx.rect(paddleX, mCanvas.height - paddleHeight, paddleWidth, paddleHeight);
        ctx.fillStyle = "#0095DD";
        ctx.fill();
        ctx.closePath();
    }

    function getBricksStatus()
    {
      var status = 0;
      for (var c = 0; c < brickColumnCount; c++) {
          for (var r = 0; r < brickRowCount; r++) {
            status= status + bricks[c][r].status;
          }
        }
      //console.log(status);
      return status;
    }
    function drawBricks() {
        for (c = 0; c < brickColumnCount; c++) {
            for (r = 0; r < brickRowCount; r++) {
                if (bricks[c][r].status >= 1) {
                    var brickX = (r * (brickWidth + brickPadding)) + brickOffsetLeft;
                    var brickY = (c * (brickHeight + brickPadding)) + brickOffsetTop;
                    bricks[c][r].x = brickX;
                    bricks[c][r].y = brickY;
                    ctx.beginPath();
                    ctx.rect(brickX, brickY, brickWidth, brickHeight);
                    // draws bricks based on status
                    switch (bricks[c][r].status) {
                        case 1: // normal brick
                            ctx.fillStyle = "#0095DD";
                            break;

                        case 2: // silver colored brick
                            ctx.fillStyle = "#C0C0C0";
                            break;
                        case 3: // golden color bricks
                            ctx.fillStyle = "#D4AF37";
                            break;
                    }
                    ctx.fill();
                    ctx.closePath();
                }
            }
        }
    }
    // paints the score on the canvas
    function drawScore() {
        ctx.font = "16px Arial";
        ctx.fillStyle = "#0095DD";
        ctx.fillText("Score: " + score, 8, 20);
    }
    // paints the lives on the canvas
    function drawLives() {
        ctx.font = "16px Arial";
        ctx.fillStyle = "#0095DD";
        ctx.fillText("Lives: " + lives, mCanvas.width - 65, 20);
    }
    // paints the level on the canvas
    function drawLevel() {
        ctx.font = "16px Arial";
        ctx.fillStyle = "#0095DD";
        ctx.fillText("Level: " + level, mCanvas.width / 2 - 65, 20);
    }
    // draws the canvas
    function draw() {
        ctx.clearRect(0, 0, mCanvas.width, mCanvas.height);
        drawBricks();
        drawBall();
        drawPaddle();
        drawScore();
        drawLives();
        drawLevel();
        collisionDetection();
        if (x + dx > mCanvas.width - ballRadius || x + dx < ballRadius) {
            dx = -dx;
        }
        if (y + dy < ballRadius) {
            dy = -dy;
        } else if (y + dy > mCanvas.height - ballRadius) {
            if (x > paddleX && x < paddleX + paddleWidth) {
                dy = -dy;
            } else {
                lives--;
                if (lives <= 0) {
                  submitScore();
                    //alert("GAME OVER");
                    return;
                    //document.location.reload();
                } else {
                    x = mCanvas.width / 2;
                    y = mCanvas.height - 30;
                    dx = speed;
                    dy = -1 * speed;
                    paddleX = (mCanvas.width - paddleWidth) / 2;
                }
            }
        }

        if (rightPressed && paddleX < mCanvas.width - paddleWidth) {
            paddleX += 7;
        } else if (leftPressed && paddleX > 0) {
            paddleX -= 7;
        }

        x += dx;
        y += dy;
        // redraws the canvas if required
        requestAnimationFrame(draw);
    }
    InitilizeGame();
    // Initializes the brick
    initializeBricks();
    draw();
    $('#submitscore').click(function() {
        submitScore();
    });
    function submitScore()
    {
      var msg = {
          "messageType": "SCORE",
          "score": parseFloat(score)
      };
      //console.log(msg.score);
      window.parent.postMessage(msg, "*");
    }
    $('#save').click(function() {
        var msg = {
            "messageType": "SAVE",
            "gameState": {
                "level": parseFloat(level),
                "score": parseFloat(score),
                "lives": parseFloat(lives),
                "bricks": JSON.stringify(bricks)
            }
        };
        //console.log(msg.gameState);
        window.parent.postMessage(msg, "*");
    });
    $('#load').click(function() {
        var msg = {
            "messageType": "LOAD_REQUEST"
        };
        window.parent.postMessage(msg, "*");
    });

    // Read incoming messages and reload the game
        window.addEventListener("message", function(e) {
            if(e.data.messageType === "LOAD") {
                loadGame(e.data.gameState);
            } else if (e.data.messageType === "ERROR") {
                alert(e.data.info);
            }
        },false);

    function loadGame(data)
    {
      //console.log('Level:'+data.level);
      level = parseFloat(data.level);
      score = parseFloat(data.score);
      lives = parseFloat(data.lives);
      bricks = $.parseJSON(data.bricks);
    }
});
