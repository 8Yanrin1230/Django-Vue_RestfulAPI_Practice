<template>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
      <div id="app">
        <h1>Debt List</h1>
        <form @submit.prevent="add">
          <div v-for="(value, key) in newDebts" :key="key">
            <div v-if="key !== 'id'">
              <label>{{ key }}</label>
              <input v-model="newDebts[key]" :placeholder="`Input ${key}`" />
            </div>
          </div>
          <button type="submit">Add</button>
        </form>

        <table class="table table-striped table-bordered">
          <thead class="thead-dark">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Total</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="debt in debts" :key="debt.DcID">
              <td>{{ debt.id }}</td>
              <td>{{ debt.UserName }}</td>
              <td>{{ debt.Total }}</td>
              <td>
                <button class="btn btn-sm btn-info" @click="get_id(debt.id)" data-bs-toggle="modal" data-bs-target="#staticBackdrop">Edit</button>
                <button class="btn btn-sm btn-danger" @click="get_id(debt.id)" data-bs-toggle="modal" data-bs-target="#staticBackdrop2">刪除</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="modal" id="staticBackdrop" tabindex="-1">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Modal title</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <div v-for="(value, key) in newDebts" :key="key">
                  <div v-if="key !== 'id'">
                  <label>{{ key }}</label>
                  <input v-model="newDebts[key]" :placeholder="`Input ${key}`" />
                </div>
              </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary">Close</button>
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="update(select_which)" >Save changes</button>
              </div>
            </div>
          </div>
        </div>


        <div class="modal" id="staticBackdrop2" tabindex="-1">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Modal title</h5>
              </div>
              <div class="modal-body">
                確定要刪除嗎
              </div>
              <div class="modal-footer">
                <button type="button" class="btn-secondary" data-bs-dismiss="modal" aria-label="Close">取消</button>
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="deleteTodo(select_which)">刪除</button>
              </div>
            </div>
          </div>
        </div>

      </div>
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