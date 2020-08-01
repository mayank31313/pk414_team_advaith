<template>
<q-page>
  <div  >
    <q-stepper
      v-model="step"
      ref="stepper"
      alternative-labels
      vertical
      color="primary"
      animated
      class="responsive full-width"
    >
      

      <q-step
        :name="1"
        title="Give type of your farm soil"
        caption="Optional"
        icon="create_new_folder"
        :done="step > 2"
      >
        <q-list>
            <q-item>
                <q-item-section>
                <q-item-label>Your Farm contain which type of soil ?</q-item-label>
                 
                    <q-select 
                    class="q-mt-sm"
                     filled 
                     dense 
                     v-model="soil" 
                     :options="soiloptions" 
                     label="Type of soil." />    
                </q-item-section>   
            </q-item>
        </q-list>
      </q-step>

      <q-step
        :name="2"
        title="Soil Health Info"
        icon="add_comment"
      >
      <legend>--- Enter soil health Information ---</legend>
        <q-form
           class="q-gutter-sm q-mt-xs"
          @submit.prevent.stop
        >
        <q-input
            dense
            filled
            type="text"
            hint="Nitrogen*"
            v-model="soilhealth.nitrogen"
            label="Amount of nitrogen in farm"
            lazy-rules
            :rules="[
              val => val !== null  || 'Required*',
    
            ]"
          > 
          </q-input>
         <q-input
            dense
            filled
            type="text"
            v-model="soilhealth.phosphorous"
            hint="Phosphorous*"
            label="Amount of phosphorous in farm"
            lazy-rules
            :rules="[
              val => val !== null  || 'Required*',
    
            ]"
          > 
          </q-input>
          <q-input
            dense
            filled
            type="text"
            hint="Organic Carbon*"
            v-model="soilhealth.organic_carbon"
            label="Amount of organic carbon in farm"
            lazy-rules 
            :rules="[
              val => val !== null  || 'Required*',
    
            ]"
          > 
          </q-input>
          <q-input
            dense
            filled
            type="text"
            v-model="soilhealth.potassium"
            hint="Potassium*"
            label="Amount of potassium in farm"
            lazy-rules
            :rules="[
              val => val !== null  || 'Required*',
    
            ]"
          > 
          </q-input>
        </q-form>
      </q-step>

      <template v-slot:navigation>
        <q-stepper-navigation>
          <q-btn @click="step===2 ? send() : $refs.stepper.next()" color="primary" :label="step === 2 ? 'Finish' : 'Continue'" />
          <q-btn v-if="step > 1" flat color="primary" @click="$refs.stepper.previous()" label="Back" class="q-ml-sm" />
        </q-stepper-navigation>
      </template>
    </q-stepper>
  </div>
   <q-inner-loading :showing="loading">
        <q-spinner size="50px" color="primary" />
    </q-inner-loading>
</q-page>
</template>
<script>
import axios from 'axios'
import  { mapActions } from 'vuex'
export default {
  created(){
    let token = window.localStorage.getItem('token')
    let username = window.localStorage.getItem('username')
    if(!token){
      this.$router.push('/')
    }else if(username==='0000000000'){
      this.$router.push('/admin')
    }
  },
  data () {
    return {
      loading:false,
      step: 1,
      accepted: [],
      soil:null,
      lat:null,
      long:null,
      soilhealth: {
        nitrogen:null,
        potassium:null,
        organic_carbon:null,
        phosphorous:null,
      },
      soiloptions:[
        {
          label: 'Black',
          value: 'black'
        },
        {
          label: 'Red',
          value: 'red'
        }
      ],
    data:null,
    }
  },
  methods:{
  
     ...mapActions('store',['cropRecommend']),
        send(){
          console.log('clicked');
          this.loading=true;
      navigator.geolocation.getCurrentPosition(this.onSuccess, this.onError);
      },
      onSuccess(position) {
        this.lat = position.coords.latitude
        this.long = position.coords.longitude
        this.cropRecommend({
        "soiltype":this.soil.value,
        "soilhealth":this.soilhealth,
        "longitude":this.long,
        "latitude":this.lat,
        "state":"haryana",
      })
      },
      // onError Callback receives a PositionError object
      //
      onError(error) {
        this.loading=false;
        console.log('code: ',error.code    + '\n' +
              'message: ' + error.message + '\n');
      },
  }
}
</script>