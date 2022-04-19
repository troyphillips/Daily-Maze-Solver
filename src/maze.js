var intervalTimer;
var app = new Vue({
    el: '#app',
    data: {
        height: 4,
        width: 4,
        bcolor: "white",
        x_c: 0,
        y_c: 0,
        time: 60,
        timeLeft: '00:00',
        endTime: 0,
        mazeData: [{
            "x": 0,
            "y": 0,
            "content": "\u2605",
            "borders": [
                1,
                0,
                0,
                1
            ]
        },
        {
            "x": 0,
            "y": 1,
            "borders": [
                0,
                1,
                0,
                0
            ]
        },
        {
            "x": 0,
            "y": 2,
            "borders": [
                1,
                0,
                0,
                1
            ]
        },
        {
            "x": 0,
            "y": 3,
            "borders": [
                1,
                1,
                0,
                0
            ]
        },
        {
            "x": 1,
            "y": 0,
            "borders": [
                0,
                1,
                0,
                1
            ]
        },
        {
            "x": 1,
            "y": 1,
            "borders": [
                0,
                1,
                1,
                1
            ]
        },
        {
            "x": 1,
            "y": 2,
            "borders": [
                0,
                1,
                0,
                1
            ]
        },
        {
            "x": 1,
            "y": 3,
            "borders": [
                0,
                1,
                0,
                1
            ]
        },
        {
            "x": 2,
            "y": 0,
            "borders": [
                0,
                0,
                1,
                1
            ]
        },
        {
            "x": 2,
            "y": 1,
            "borders": [
                1,
                0,
                0,
                0
            ]
        },
        {
            "x": 2,
            "y": 2,
            "borders": [
                0,
                1,
                1,
                0
            ]
        },
        {
            "x": 2,
            "y": 3,
            "borders": [
                0,
                1,
                0,
                1
            ]
        },
        {
            "x": 3,
            "y": 0,
            "borders": [
                1,
                0,
                1,
                1
            ]
        },
        {
            "x": 3,
            "y": 1,
            "borders": [
                0,
                1,
                1,
                0
            ]
        },
        {
            "x": 3,
            "y": 2,
            "borders": [
                1,
                0,
                0,
                1
            ]
        },
        {
            "x": 3,
            "y": 3,
            "borders": [
                0,
                1,
                1,
                0
            ]
        }]
    },
    methods: {
        setTime(seconds) {
          clearInterval(intervalTimer);
          this.timer(seconds);
        },
        timer(seconds) {
          const now = Date.now();
          const end = now + seconds * 1000;
          this.displayTimeLeft(seconds);
    
          this.endTime = seconds;
          this.countdown(end);
        },
        countdown(end) {
          intervalTimer = setInterval(() => {
            const secondsLeft = Math.round((end - Date.now()) / 1000);
    
            if(secondsLeft === 0) {
              this.endTime = 0;
            }
    
            if(secondsLeft < 0) {
              clearInterval(intervalTimer);
              return;
            }
            this.displayTimeLeft(secondsLeft)
          }, 1000);
        },
        displayTimeLeft(secondsLeft) {
          const minutes = Math.floor(secondsLeft / 60);
          const seconds = secondsLeft % 60;
    
          this.timeLeft = `${minutes}:${seconds}`;
        },
        moveRight: function () {
            if (this.mazeData[this.mazeIndex].borders[1] == 0) {
                this.mazeData[this.mazeIndex].content = "\u2606";
                this.$set(this, "y_c", this.y_c + 1);
                this.mazeData[this.mazeIndex].content = "\u2605";
            }
        },
        moveLeft: function () {
            if (this.mazeData[this.mazeIndex].borders[3] == 0) {
                this.mazeData[this.mazeIndex].content = "\u2606";
                this.$set(this, "y_c", this.y_c - 1);
                this.mazeData[this.mazeIndex].content = "\u2605";
            }
        },
        moveDown: function () {
            if (this.mazeData[this.mazeIndex].borders[2] == 0) {
                this.mazeData[this.mazeIndex].content = "\u2606";
                this.$set(this, "x_c", this.x_c + 1);
                this.mazeData[this.mazeIndex].content = "\u2605";
            }
        },
        moveUp: function () {
            if (this.mazeData[this.mazeIndex].borders[0] == 0) {
                this.mazeData[this.mazeIndex].content = "\u2606";
                this.$set(this, "x_c", this.x_c - 1);
                this.mazeData[this.mazeIndex].content = "\u2605";
            }
        },
        startMaze: function () {
                this.$set(this, "bcolor", "black");
        }
    },
    created() {
        var self = this
        $.getJSON('src/maze.json', function (data) {
            self.height = data.height;
            self.weight = data.weight;
            self.mazeData = data.cells;
            self.messsage = "data loaded";
        });
    }
});  
