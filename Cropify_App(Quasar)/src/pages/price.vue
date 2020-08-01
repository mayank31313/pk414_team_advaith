<template>
<q-page>
    <div class="full-width">
        <!-- <GChart
        class="q-pa-sm"
        type="LineChart"
        :data="chartData"
        :options="chartOptions"
        /> -->
    </div>
    <div>
      <line-chart :data="chartkickdata" :colors="['#228B22']" />
    </div>
</q-page>
</template>
<script>

import axios from 'axios'
import { GChart } from 'vue-google-charts'
import  { mapActions } from 'vuex'
export default {
    created(){
        return axios.get('http://10.8.0.10:8000/api/price/')
        .then(response => {
          console.log(response)
          let data = new Array()
          data.push(['Crop name', 'Price'])
          if(response.status == 200){
            for (let i=0;i<response.data.length;i++){
                let price = response.data[i].prices
                for(let key in price){
                  data.push([key,price[key]])
                }            
            }
            // console.log(data)
            // this.chartData = data
          }
        })
    },
    data(){
        return {
          chartkickdata:[
          {name: '2020-08-01 Price', data:{
"Barley": 157.40786743164062,
"Cashew nut": 158.02830505371094,
"Coffee": 104.53758239746094,
"Cotton": 104.90695190429688,
"Jowar": 160.4559783935547,
"Jute": 206.333251953125,
"Maize": 148.13819885253906,
"Paddy": 162.33460998535156,
"Pulses": 158.79295349121094,
"Rape & Mustard": 150.5597381591797,
"Rubber": 56.834739685058594,
"Sugarcane": 166.0834197998047,
"Tea": 155.21543884277344,
"Tobacco": 113.47625732421875,
"Wheat": 156.363525390625
        }},
          // {name: 'Call parents', data: {'2017-01-01': 5, '2017-01-02': 3}}
        ],
        chartData: [
            ['Crop name', 'Price'],
            // ["Barley", 157.40786743164062,158.02830505371094,158.02830505371094],
            
            // ["",158.02830["",158.02830505371094],
            // ["",158.02830505371094],505371094],
            // ["Cashew nut", 158.02830505371094],
            // ["Coffee",104.53758239746094],
            // ["Cotton", 104.90695190429688],
            // ["Jowar", 160.4559783935547],
            // ["Jute", 206.333251953125],
            // ["Maize", 148.13819885253906],
            // ["Paddy", 162.33460998535156],
            // ["Pulses", 158.79295349121094],
            // ["Rape & Mustard", 150.5597381591797],
            // ["Rubber", 56.834739685058594],
            // ["Sugarcane", 166.0834197998047],
            // ["Tea", 155.21543884277344],
            // ["Tobacco", 113.47625732421875],
            // ["Wheat", 156.363525390625],
        ],
      chartOptions: {
        chart: {
          title: 'Company Performance',
          subtitle: 'Sales, Expenses, and Profit: 2014-2017',
        }
      }
        }
    },
    methods:{
      ...mapActions('store',['PricePrediction']),
    // price(){
    //  this.PricePrediction(this.data)
    // }
  }
}
</script>