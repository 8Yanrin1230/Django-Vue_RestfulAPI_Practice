<template>
  <div id="Debts">

  <table class="table table-striped table-bordered">
      <thead class="thead-dark">
        <tr>
          <th>Debtor</th>
          <th>Creditor</th>
          <th>Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="debt in debts" :key="debt.id">
          <td>{{ debt.debtor_id }}</td>
          <td>{{ debt.creditor_id }}</td>
          <td>{{ debt.amount }}</td>
          <td>
              <button class="btn btn-sm btn-danger" @click="delete_debt(debt)" data-bs-toggle="modal" data-bs-target="#staticBackdrop2">刪除</button>
            </td>
        </tr>
      </tbody>
  </table>

  </div>
</template>

<script>
import axios from 'axios'
class Debts {
  constructor(debtor_id,creditor_id,amount) {
   this.debtor_id = debtor_id
   this.creditor_id = creditor_id
   this.amount = amount
  }
}

export default {
  name: 'Debts',
  data() {
    return {
      debts: [],

      }
    },
  mounted() {
    this.fetch()
  },

  methods: {
   async fetch() {
      axios.get('http://127.0.0.1:8000/api/debts')
        .then(response => {
          this.debts = response.data.map(debt => new Debts(
            debt.debtor_id,
            debt.creditor_id,
            debt.amount,
          ));
        })
        .catch(error => {
          console.error(error)
        })
    },
    async delete_debt(debt) {
      const recordData = {
        debtors: debt.debtor_id,
        creditors: debt.creditor_id,
        amount: debt.amount
      };

      axios.delete('http://127.0.0.1:8000/api/debts' ,{data: recordData})
      .then(response =>{
        this.fetch()

      })
            .catch(error => {
              console.error(error)
            })
        },
      }
    }
</script>