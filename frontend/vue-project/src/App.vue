<template>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Navbar</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <router-link to="/Records" class="nav-link active" aria-current="page">Records</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/Debts" class="nav-link">Debts</router-link>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Dropdown
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
          <div v-for="debt in debts">
            <li>
              <router-link to="/Debts" class="dropdown-item">{{debt.UserName}}</router-link>
            </li>
          </div>
          </ul>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled">Disabled</a>
        </li>
      </ul>

    </div>
  </div>
</nav>

    <router-view></router-view>
</template>
<script>
import axios from 'axios'

class Tag {
  constructor(id,DcID, UserName, Record, Account, PokerID, Total, clear, WOL) {
    this.id = id;
    this.DcID = DcID;
    this.UserName = UserName;
    this.Record = Record;
    this.Account = Account;
    this.PokerID = PokerID;
    this.Total = Total;
    this.clear = clear;
    this.WOL = WOL;
  }
}

export default {
  name: 'App',
  data() {
    return {
      debts: [],
      newDebts:{
        id: 0,
        DcID: '',
        UserName: '',
        Record: '',
        Account: '',
        PokerID: '',
        Total:0,
        clear: false,
        WOL: true
      },
      select_which:Number
    }
  },
  mounted() {
    this.fetch()
  },

  methods: {
   async fetch() {
      axios.get('http://127.0.0.1:8000/api/debts')
        .then(response => {
          this.debts = response.data.map(debt => new Tag(
            debt.id,
            debt.DcID,
            debt.UserName,
            debt.Record,
            debt.Account,
            debt.PokerID,
            debt.Total,
            debt.clear,
            debt.WOL,
          ));
        })
        .catch(error => {
          console.error(error)
        })
    },
   async add() {
      axios.post('http://127.0.0.1:8000/api/debts',this.newDebts)
        .then(response => {
          this.debts.push(this.newDebts);
          window.location.reload();
        })
        .catch(error => {
          console.error(error)
        })
    },
    update(id) {
      this.newDebts.id = id
      axios.put(`http://127.0.0.1:8000/api/debts/${id}`,this.newDebts)
        .then(response =>{
          this.debts.push(this.newDebts);
          window.location.reload();
        })
        .catch(error => {
          console.error(error)
        })
    },
    deleteTodo(id) {
      axios.delete(`http://127.0.0.1:8000/api/debts/${id}`)
        .then(() => {
          this.debts = this.debts.filter(debt => debt.id !== id)
          window.location.reload();
        })
        .catch(error => {
          console.error(error)
        })
    },
    get_id(id){this.select_which = id},
  }
}
</script>