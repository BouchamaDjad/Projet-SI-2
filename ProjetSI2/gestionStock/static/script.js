$(function () {
    $(document).ready(function () {
        $('#search').DataTable();
    });
});

$(function () {
    $(document).ready(function () {
        $('#noSearch').DataTable({
            "searching":false,
        });
    });
});



$(function () {
    $(document).ready(function () {
        $('#dernier').DataTable({
            columnDefs: [
                { orderable: false,"searchable": false, "targets":-1},
            ]
        });
    });
});

$(function () {
    $(document).ready(function () {
        $('#deuxF').DataTable({
            columnDefs: [
                { "searchable": false, "targets":[2,3,4,5]},
            ]
        });
    });
});

Urls = [
    { nom: "Vente au comptoire", url:"http://127.0.0.1:8000/SelectionClient/" },
    { nom: "Paiement Credit", url:"http://127.0.0.1:8000/ReglementVentes/" },
    { nom: "Bon de commande", url: "http://127.0.0.1:8000/BonCommande/" },
    { nom: "Saisir Facture", url:"http://127.0.0.1:8000/SaisieFacture/" },
    { nom: "Reglement de facture", url:"http://127.0.0.1:8000/ReglementFactures/" },
    { nom: "Journal Achats", url: "http://127.0.0.1:8000/listeFactures/" },
    { nom: "Journal Reglement Facture", url: "http://127.0.0.1:8000/journalReglement/" },
    { nom: "liste clients", url:"http://127.0.0.1:8000/Clients/" },
    { nom: "Ajout client", url:"http://127.0.0.1:8000/CreationClient/" },
    { nom: "Liste Fournisseurs", url:"http://127.0.0.1:8000/Fournisseurs/" },
    { nom: "Ajout fournisseur", url:"http://127.0.0.1:8000/AjouterFournisseur/" },
    { nom: "Consulter Stock", url:"http://127.0.0.1:8000/Stock/" },
    { nom: "Entrees stock", url:"http://127.0.0.1:8000/EntréeStock/" },
    { nom: "Sorties stock", url:"http://127.0.0.1:8000/SortieStock/" },
    { nom: "Ajout Produit", url:"http://127.0.0.1:8000/AjouterProduits/" },
    { nom: "Liste des Produits", url: "http://127.0.0.1:8000/listeProduits/" },
    { nom: "Liste Types Produits" ,url:"http://127.0.0.1:8000/TypesProduits/"},
    { nom: "Ajout Type produit", url:"http://127.0.0.1:8000/AjouterType/" },
    { nom: "stats Ventes", url:"http://127.0.0.1:8000/Stats/" },
    { nom: "stats Achats", url:"http://127.0.0.1:8000/StatsAchats/" },
]

function getUrl(nom){
    url = Urls.find(element => element.nom==nom)
    if(url) return url.url
    else return ""
}


list = getFavs()

function toggleFavs() {
    let overlay = document.querySelector(".overlay");
    overlay.classList.toggle('d-none');
    let container = document.querySelector(".containerF");
    container.classList.toggle('d-none');
}

let c = document.querySelector("#close")
let w = document.querySelector("#wheel")


function clearContent() {
    let container = document.querySelector('.urls');
    container.replaceChildren();
}

function populate() {
      container = document.querySelector(".urls")
      Urls.forEach(url =>  {
      opt = document.createElement("div")
      opt.className = "opt d-flex justify-content-between"
      nom = document.createElement("div")
      nom.className = "nomUrl"
      nom.textContent = url.nom;
      input = document.createElement("input")
      input.type = "checkbox"
      input.className="checkF"
      input.value =url.nom
      if(checkInFavoris(input.value)) input.checked=true;
      opt.append(nom,input)
      container.append(opt)
  })
}

function checkInFavoris(nom){
    return list.some(url => url.nom == nom);
}

c.addEventListener("click",(e)=>{
    toggleFavs()
    updateFavs()
    clearContent()
    displayFavoris()
})

function favoris(nom,url){
    this.nom = nom;
    this.url = url;
}

function updateFavs(){
    checked = getCheckedBoxes()
    list = []
    if(checked){
        checked.forEach(element => {
          url = getUrl(element.value)
          f = new favoris(element.value, url)
          list.push(f)
        }) 
    }
    updateStorage(list)
}

function getCheckedBoxes() {
    let checkboxes = document.querySelectorAll(".checkF");
    let checkboxesChecked = [];
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            checkboxesChecked.push(checkboxes[i]);
        }
    }
    return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}


function displayFavoris() {
    container = document.querySelector("#favoris")
    container.replaceChildren()
    list.forEach(element => {
        a = document.createElement("a")
        a.className = "link-dark d-inline-flex text-decoration-none rounded"
        a.href = element.url
        a.textContent = element.nom
        li = document.createElement("li")
        li.append(a)
        container.append(li)
    })
}


w.addEventListener("click", (e) => {
    toggleFavs()
    populate()
})

function addFavs(nom) {
    newFav = favoris(nom,url)
    list.append(newFav)
}

function updateStorage(favoris){
    let newFav = JSON.stringify(favoris);
    localStorage.removeItem('favoris');
    localStorage.favoris = newFav;
}

function getFavs() {
    if (localStorage.getItem("favoris")) {
        return JSON.parse(localStorage.favoris);
    }
    else return [];
}

displayFavoris()