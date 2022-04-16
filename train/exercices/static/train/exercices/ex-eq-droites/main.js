
function pgcd(a, b) {
    while (b != 0) {
        let t = b;
        b = a % b;
        a = t;
    }

    return a;
}

EXERCICE_PLAYER.register ( 'eq-droites', function generator ( html ) {

    // generate ax + by = c, with a, b, c in [[-3; 3[[

    let a = 0;
    let b = 0;
    let c = 0;
    
    while (true) {
        while (a == 0 && b == 0) {
            a = Math.floor(Math.random() * 7) % 7 - 3
            b = Math.floor(Math.random() * 7) % 7 - 3
            c = Math.floor(Math.random() * 7) % 7 - 3
        }

        if (a != 0 && b != 0) break
        if (Math.random() < (1 / 9)) break
    }

    let divider = pgcd(pgcd(a, b), c)

    return { a, b, c, html }

}, function show_exercice(exercice) {
    EXERCICE_PLAYER.get_exercice_container().innerHTML = (exercice.html.split("<solhidden>")).join("hidden")
    
    let canvas = new GeometryCanvas(600, 600, EXERCICE_PLAYER.get_exercice_container().querySelector('#canvas-container'))
    
    canvas.generateAxis(-5, 5, -5, 5)
    let line_func = (x, y) => { return exercice.a * x + exercice.b * y }
    let null_func = (x, y) => exercice.c
    canvas.setStroke("#aa3333")
    canvas.drawEqual(line_func, null_func)
}, function show_solution (exercice) {
    EXERCICE_PLAYER.get_exercice_container().innerHTML = (exercice.html.split("<solhidden>")).join("").replace("<%a%>", exercice.a).replace("<%b%>", exercice.b).replace("<%c%>", exercice.c)
    EXERCICE_PLAYER.timer=0;
    let canvas = new GeometryCanvas(600, 600, EXERCICE_PLAYER.get_exercice_container().querySelector('#canvas-container'))

    canvas.generateAxis(-5, 5, -5, 5)

    let line_func = (x, y) => { return exercice.a * x + exercice.b * y }
    let null_func = (x, y) => exercice.c
    
    canvas.setStroke("#aa3333")
    canvas.drawEqual(line_func, null_func)

    let { a, b, c } = exercice

    // ax + by = c
    // y = c / b
    let lx = 0
    let ly = c / b

    // ax + by = c
    // x = -b => y = c / b + a
    let rx = b
    let ry = c / b - a

    canvas.setStroke("#33aa33")
    canvas.drawEqual((x, y) => y, (x, y) => ly, sx=[lx, ly - 1], ex=[rx, ly + 1])
    canvas.drawEqual((x, y) => x, (x, y) => rx, sx=[rx - 1, ly], ex=[rx + 1, ry])
} )
