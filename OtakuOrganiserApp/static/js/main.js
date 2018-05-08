

var modal = document.getElementById('{{ anime.anime_id }}-' + 'myModal');
var Authmodal = document.getElementById('{{ anime.anime_id }}-' + 'delmodal');
var btn = document.getElementById( "{{ anime.anime_id }}-" + "myBtn");
var Delbtn = document.getElementById( "{{ anime.anime_id }}-" + "deletebtn");
var span = document.getElementsByClassName("close")[0];
btn.onclick = function() {
    modal.style.display = "block";
}
Delbtn.onclick = function() {
    Authmodal.style.display = "block";
}
span.onclick = function() {
    modal.style.display = "none";
    Authmodal.style.display = "none";
}
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
    if (event.target == Authmodal) {
        Authmodal.style.display = "none";
    }
}

function AuthModal ()
{
    Authmodal.style.display = "block";
}

function spanClose () {
    modal.style.display = "none";
    Authmodal.style.display = "none";
}

function windowClose (event) 
{
    if (event.target == modal) {
        modal.style.display = "none";
    }
    if (event.target == Authmodal) {
        Authmodal.style.display = "none";
    }
}

function deleteRecord() 
{
    if(confirm("Are you sure you want to remove {{anime.name}} record?") == true)
    {
        window.location.href = "{% url 'delete' anime.pk %}";
    }
}