var app = new Vue({
    el: '#app',
    data: {
        message: 'This is a simple Vue.js Declarative Rendering example!',
        height: 4,
        width: 4,
        mazeData: [{
            "x": 0,
            "y": 0,
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
    /*mounted() {
        var self = this
        $.getJSON('maze.json', function (data) {
            self.height = data.height;
            self.weight = data.weight;
            self.mazeData = data.cells;
        });
    }*/
});  
