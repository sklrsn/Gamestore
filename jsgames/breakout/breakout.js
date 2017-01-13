$(document).ready(function(){
  var canvas = $("#gameCanvas");
  var mCanvas = canvas[0];
  var ctx = mCanvas.getContext("2d");
  ctx.canvas.width  = 400;//window.innerWidth;
  ctx.canvas.height = 640;//window.innerHeight;
  var ballRadius = 10;
  var x = mCanvas.width/2;
  var y = mCanvas.height-30;
  var speed = 3;
  var dx = speed;
  var dy = -1*speed;
  var paddleHeight = 10;
  var paddleWidth = 75;
  var paddleX = (mCanvas.width-paddleWidth)/2;
  var rightPressed = false;
  var leftPressed = false;
  var brickRowCount = 5;
  var brickColumnCount = 3;
  var brickWidth = ctx.canvas.width/6;
  var brickHeight = ctx.canvas.height/40;
  var brickPadding = 10;
  var brickOffsetTop = 30;
  var brickOffsetLeft = 30;
  var score = 0;
  var lives = 3;
  var level = 1;

  var bricks = [];
  function initializeBricks()
  {
    for(c=0; c<brickColumnCount; c++) {
        bricks[c] = [];
        for(r=0; r<brickRowCount; r++) {
            bricks[c][r] = { x: 0, y: 0, status: 1 };
        }
    }
  }
initializeBricks();
  $(this).keyup(function(e){
    if(e.keyCode == 39) {
        rightPressed = false;
    }
    else if(e.keyCode == 37) {
        leftPressed = false;
    }
  });
  $(this).keydown(function(e){
    if(e.keyCode == 39) {
        rightPressed = true;
    }
    else if(e.keyCode == 37) {
        leftPressed = true;
    }
  });
  $(this).mousemove(function(e){
    var relativeX = e.clientX - mCanvas.offsetLeft;
    if(relativeX > 0 && relativeX < mCanvas.width) {
        paddleX = relativeX - paddleWidth/2;
    }
  });

  function collisionDetection() {
      for(c=0; c<brickColumnCount; c++) {
          for(r=0; r<brickRowCount; r++) {
              var b = bricks[c][r];
              if(b.status == 1) {
                  if(x > b.x && x < b.x+brickWidth && y > b.y && y < b.y+brickHeight) {
                      dy = -dy;
                      b.status = 0;
                      score++;
                      if(score/level == brickRowCount*brickColumnCount) {
                          level++;
                          speed+=1;
                          dx = speed;
                          dy = -1*speed;
                          paddleX=(mCanvas.width-paddleWidth)/2;
                          x = mCanvas.width/2;
                          y = mCanvas.height-30;
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
      ctx.arc(x, y, ballRadius, 0, Math.PI*2);
      ctx.fillStyle = "#0095DD";
      ctx.fill();
      ctx.closePath();
  }
  function drawPaddle() {
      ctx.beginPath();
      ctx.rect(paddleX, mCanvas.height-paddleHeight, paddleWidth, paddleHeight);
      ctx.fillStyle = "#0095DD";
      ctx.fill();
      ctx.closePath();
  }
  function drawBricks() {
      for(c=0; c<brickColumnCount; c++) {
          for(r=0; r<brickRowCount; r++) {
              if(bricks[c][r].status == 1) {
                  var brickX = (r*(brickWidth+brickPadding))+brickOffsetLeft;
                  var brickY = (c*(brickHeight+brickPadding))+brickOffsetTop;
                  bricks[c][r].x = brickX;
                  bricks[c][r].y = brickY;
                  ctx.beginPath();
                  ctx.rect(brickX, brickY, brickWidth, brickHeight);
                  ctx.fillStyle = "#0095DD";
                  ctx.fill();
                  ctx.closePath();
              }
          }
      }
  }
  function drawScore() {
      ctx.font = "16px Arial";
      ctx.fillStyle = "#0095DD";
      ctx.fillText("Score: "+score, 8, 20);
  }
  function drawLives() {
      ctx.font = "16px Arial";
      ctx.fillStyle = "#0095DD";
      ctx.fillText("Lives: "+lives, mCanvas.width-65, 20);
  }
  function drawLevel(){
    ctx.font = "16px Arial";
    ctx.fillStyle = "#0095DD";
    ctx.fillText("Level: "+level, mCanvas.width/2-65, 20);
  }

  function draw() {
      ctx.clearRect(0, 0, mCanvas.width, mCanvas.height);
      drawBricks();
      drawBall();
      drawPaddle();
      drawScore();
      drawLives();
      drawLevel();
      collisionDetection();

      if(x + dx > mCanvas.width-ballRadius || x + dx < ballRadius) {
          dx = -dx;
      }
      if(y + dy < ballRadius) {
          dy = -dy;
      }
      else if(y + dy > mCanvas.height-ballRadius) {
          if(x > paddleX && x < paddleX + paddleWidth) {
              dy = -dy;
          }
          else {
              lives--;
              if(lives<=0) {
                  alert("GAME OVER");
                  return;
                  //document.location.reload();
              }
              else {
                  x = mCanvas.width/2;
                  y = mCanvas.height-30;
                  dx = speed;
                  dy = -1*speed;
                  paddleX = (mCanvas.width-paddleWidth)/2;
              }
          }
      }

      if(rightPressed && paddleX < mCanvas.width-paddleWidth) {
          paddleX += 7;
      }
      else if(leftPressed && paddleX > 0) {
          paddleX -= 7;
      }

      x += dx;
      y += dy;
      requestAnimationFrame(draw);
  }
  draw();
});
