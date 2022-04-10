
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
    
    while (a == 0 && b == 0) {
        a = Math.floor(Math.random() * 7) % 7 - 3
        b = Math.floor(Math.random() * 7) % 7 - 3
        c = Math.floor(Math.random() * 7) % 7 - 3
    }

    let divider = pgcd(pgcd(a, b), c)
    a /= divider
    b /= divider
    c /= divider

    return { a, b, c, html }

}, function show_exercice(exercice) {
    EXERCICE_PLAYER.get_exercice_container().innerHTML = (exercice.html.split("<solhidden>")).join("hidden")
    
    let canvas = new GeometryCanvas(600, 600, EXERCICE_PLAYER.get_exercice_container().querySelector('#canvas-container'))
    
    canvas.drawAxis(-5, -5, 5, 5)
    canvas.drawLine(exercice.a, exercice.b, exercice.c)
}, function show_solution (exercice) {
    EXERCICE_PLAYER.get_exercice_container().innerHTML = (exercice.html.split("<solhidden>")).join("").replace("<%a%>", exercice.a).replace("<%b%>", exercice.b).replace("<%c%>", exercice.c)

    let canvas = new GeometryCanvas(600, 600, EXERCICE_PLAYER.get_exercice_container().querySelector('#canvas-container'))

    canvas.drawAxis(-5, -5, 5, 5)
    canvas.drawLine(exercice.a, exercice.b, exercice.c)

    let { a, b, c } = exercice

    // ax + by = c
    // y = c / b
    let lx = 0
    let ly = c / b

    // ax + by = c
    // x = -b => y = c / b + a
    let rx = -b
    let ry = c / b - a

    canvas.drawSegment(lx, ly, rx, ly)
    canvas.drawSegment(rx, ly, rx, ry)
} )
