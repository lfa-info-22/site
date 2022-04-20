document.onkeyup = function(e) {
    coder2();
};
window.onload=update_car2;
function update_car2() {
    let a = document.getElementById("caracteristiques2");
    let b = document.getElementById("bouton-automatique2");
    b.innerHTML = "";
    a.innerHTML = "";

    if(document.getElementById("estPrems").checked) {
        a.innerHTML = '<label for="nb" class="joli-texte">Nombre :</label><input type="text" id="nb" name="nb" placeholder="47" onkeyup="coder()">';
    } 
    else if( document.getElementById("diviseurs").checked) {
        a.innerHTML = '<label for="nb" class="joli-texte">Nombre :</label><input type="text" id="nb" name="nb" placeholder="47" onkeyup="coder()">';
    }
    else if( document.getElementById("nbspremsjusquan").checked) {
        a.innerHTML = '<label for="nb" class="joli-texte">Nombre :</label><input type="text" id="nb" name="nb" placeholder="47" onkeyup="coder()">';
    }
    else if( document.getElementById("autreBase").checked) {
        a.innerHTML = '<label for="nb" class="joli-texte">Nombre :</label><input type="text" id="nb" name="nb" placeholder="47" onkeyup="coder()"><br/><label for="nb2" class="joli-texte">Base de départ :</label><input type="text" id="nb2" name="nb2" placeholder="47" onkeyup="coder()"><br/><label for="nb3" class="joli-texte">Base dans laqulle convertir :</label><input type="text" id="nb3" name="nb3" placeholder="47" onkeyup="coder()">';
    }
    else if (document.getElementById("farey_approximation").checked) {
        a.innerHTML = '<label for="nb" class="joli-texte">Nombre :</label><input type="text" id="nb" name="nb" placeholder="47" onkeyup="coder()">';
    }
    else if(document.getElementById("pgcd").checked) {
        a.innerHTML = '<label for="nb" class="joli-texte">Nombre :</label><input type="text" id="nb" name="nb" placeholder="47" onkeyup="coder()"><br/><label for="nb2" class="joli-texte">2ème nombre :</label><input type="text" id="nb2" name="nb2" placeholder="47" onkeyup="coder()">';
    }
    coder2();
}

function coder2() {
    let nb = stringtoint(document.getElementById("nb").value);
    let message = "";

    if(nb <= 0) {
        return ;
    }

    if(document.getElementById("estPrems").checked) {
        if(estPrems(nb)) {
            message = nb + " est premier"
        }
        else {
            message = nb + " n'est pas premier"
        }
    } 
    else if(document.getElementById("diviseurs").checked) {
        let a = diviseurs(nb);
        message = "Liste des diviseurs de " + nb + " : <br/>"
        for(let i = 0; i < a.length; i++) {
            message += a[i] + ", "
        }
        message += nb;
    }
    else if(document.getElementById("nbspremsjusquan").checked) {
        let a = NbsPremsjusquaN(nb);
        message = "Liste des nombres premiers jusqu'à " + nb + " : <br/>"
        for(let i = 0; i < a.length; i++) {
            message += a[i] + ", "
        }
    } 
    else if(document.getElementById("autreBase").checked) {
        let nb2 = stringtoint(document.getElementById("nb2").value);
        let nb3 = stringtoint(document.getElementById("nb3").value);
        if(nb2 <= 1 || nb3 <= 1 ) {
            return ;
        }
        message = nb + " de la base " + nb2 + " vers la base " + nb3 + " : " + convertBase(nb.toString(), nb2, nb3)
    }
    else if(document.getElementById("farey_approximation").checked) {
        message = farey_approximation(nb, 99999999)
    }
    else if(document.getElementById("pgcd").checked) {
        let nb2 = stringtoint(document.getElementById("nb2").value);
        if(nb2 <= 0) {
            return ;
        }
        message = "Le PGCD de " + nb + " et " + nb2 + " est " + pgcd(nb,nb2);
    }

    document.getElementById("result2").innerHTML = "<p class=\"texte-blanc\">" + message + "</p>" + '<img id="copy" src="../../static/articles/outils/copy.png" alt="copy icon" style="width:25px;height:25px;" onclick="copyResultOnClipboard()" >';
}

//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////// LES FONCTIONS POUR CODER ET TT :  ///////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

function stringtoint(string, nb_defaut = 0) {
    nb = nb_defaut;
    if (! isNaN(Number(string)) && string != "")
    {
        nb = Number(string);
    }
    return nb
}


function convertBase(value, from_base, to_base) {
    var range = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/'.split('');
    var from_range = range.slice(0, from_base);
    var to_range = range.slice(0, to_base);
    
    var dec_value = value.split('').reverse().reduce(function (carry, digit, index) {
      if (from_range.indexOf(digit) === -1) throw new Error('Invalid digit `'+digit+'` for base '+from_base+'.');
      return carry += from_range.indexOf(digit) * (Math.pow(from_base, index));
    }, 0);
    
    var new_value = '';
    while (dec_value > 0) {
      new_value = to_range[dec_value % to_base] + new_value;
      dec_value = (dec_value - (dec_value % to_base)) / to_base;
    }
    return new_value || '0';
  }

  function estPrems(n) {
    // Corner cases
    if (n <= 1)
        return false;
    if (n <= 3)
        return true;
  
    // This is checked so that we can skip
    // middle five numbers in below loop
    if (n % 2 == 0 || n % 3 == 0)
        return false;
  
    for (let i = 5; i * i <= n; i = i + 6)
        if (n % i == 0 || n % (i + 2) == 0)
            return false;
  
    return true;
  }

  function diviseurs(nombre) {
      let nb_diviseurs = new Array();
      for(let i = 0; i < nombre; i++) {
          if(nombre % i == 0) {
              nb_diviseurs.push(i);
          }
      }
      return nb_diviseurs;
  }

  function NbsPremsjusquaN(nombre) {
      let nbprems = new Array();
      nbprems.push(2);

      for(let i = 3; i <= nombre; i++) {
          let estprems = true;
          let nb2 = 0;
          let sqrt_num = Math.sqrt(i);

          while(estprems && (nb2 < nbprems.length) && (nbprems[nb2] <= sqrt_num)) {
              if( i % nbprems[nb2] == 0 ) {
                  estprems = false;
              }
              nb2++;
          } 

          if (estprems) {
              nbprems.push(i);
          }
      }

      return nbprems;
  }

  function farey_approximation(nombre, precision = 10000) {
    let nb_int = Math.floor(nombre);
    let nb2 = nombre - nb_int;
    let num_below = 0, den_below = 1, num_above = 1, den_above = 1, num_mediant = 1, den_mediant = 2;

    while (num_mediant < precision && den_mediant < precision)
    {
        if(nb2 > num_mediant/den_mediant)
        {
            num_below = num_mediant;
            den_below = den_mediant;
            num_mediant = num_mediant + num_above;
            den_mediant = den_mediant + den_above;
        }
        else
        {
            num_above = num_mediant;
            den_above = den_mediant;
            num_mediant = num_mediant + num_below;
            den_mediant = den_mediant + den_below;
        }
    }

    return (num_mediant + nb_int*den_mediant).toString() + "/" + (den_mediant).toString();
  }

  function pgcd(a,  b)
{
    if (b == 0)
        return a;
    return pgcd(b,a%b);
}