<template>
  <q-page class="animate_animated animate_slideInRight full-width" >
      <div class="q-pa-md text-center " >
        <label class="text-h6 text-primary my-font">
          Production Details
        </label>
        <q-form
          @submit.prevent.stop="onSubmit"
          class="q-gutter-xs q-pa-md q-mt-xl" 
        >
        <q-select
            label="Select crop"
            transition-show="flip-up"
            transition-hide="flip-down"
        
            dense
            v-model="product.crop"
            :options="options"
        >
            <template v-slot:prepend>
            <q-avatar square  size="sm"><q-img no-default-spinner src="statics/crops.png"/></q-avatar>
            </template>
        </q-select>
        <q-input
            dense
            type="text"
            v-model="product.quantity"
            class="q-mt-md"
            label="Quantity in KG"
            lazy-rules
    
            :rules="[
              val => val !== null  || 'Please Enter the quantity.',
    
            ]"
          > 
             <template v-slot:prepend>
                <q-avatar><q-img no-default-spinner src="statics/kg.png" /></q-avatar>
            </template>
          </q-input>
          
          
          <div v-if="this.product.click==false"> 
             <q-btn class="full-width" label="Continue" type="submit" color="primary"/>
          </div>
          <div v-else>
            <q-spinner-facebook
              color="primary"
              size="2em"
            />
          </div>

        </q-form>
        
      </div>
  </q-page>
</template> 

<script>
import axios from 'axios'
import  { mapActions } from 'vuex'
export default {
  data(){
    return{
    product:{
      crop:null,
      quantity:null,
      click:false
    },
     options:
     [
      "sugarcane",
      "cotton",
      "tobacco",
      "rice",
      "cashewnuts",
      "tea",
      "coffee",
      "rubber",
      "wheat",
      "barley",
      "rape",
      "millets maize",
      "pulses",
      "jowar",
      "jute",

     ],
    }
  },
  methods:{
      ...mapActions('store',['production']),
    onSubmit(){
      this.product.click=true
     this.production(this.product)
    }
  }
}
</script>
<style>
@import url('https://fonts.googleapis.com/css?family=Amarante');
@import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.0.0/animate.min.css');
.animate_animated.animate_slideInRight {
  --animate-duration: 1s;
}
</style>
