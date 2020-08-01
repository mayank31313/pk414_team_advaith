<template>
  <q-page class="animate_animated animate_slideInRight" >
      <div class="q-pa-md text-center" >
        <label class="text-h4 text-primary my-font">
          Register
        </label>
        <q-form
          @submit.prevent.stop="onSubmit"
          class="q-gutter-xs q-pa-xs q-mt-xs" 
        >
        <q-input
            dense
            type="text"
            v-model="user.name"
            class="q-mt-md"
            label="Your Name*"
            lazy-rules
    
            :rules="[
              val => val !== null  || 'Please type your Full Name.',
    
            ]"
          > 
             <template v-slot:prepend>
                      <q-icon name="far fa-user" color="grey" />
                    </template>
          </q-input>
          <q-input
            dense
            type="tel"
            v-model="user.phone"
            label="Your phone*"
            lazy-rules
            maxlength="10"
            :rules="[
              val => val !== null  || 'Please type your phone no.',
              val => val.length===10 || 'Please type a valid phone.'
            ]"
          > 
             <template v-slot:prepend>
                       <q-icon name="phone" color="grey" />
                    </template>
          </q-input>
          <q-input
            dense
            type="text"
            v-model="user.city"
            label="City/District*"
            lazy-rules
    
            :rules="[
              val => val !== null  || 'Please enter your city.',
    
            ]"
          > 
             <template v-slot:prepend>
                      <q-icon name="apartment" color="grey" />
                    </template>
          </q-input>
          
          <q-input
                  type="text"
                  ref="pincode"
                 dense
                  maxlength="6"
                  v-model="user.pincode"
                  label="Pincode*"
                  lazy-rules
                  :rules="[
                    val => val != null && val.length == 6 || 'Please enter a valid pincode',
                  ]"
                >
                  <template v-slot:prepend>
                    <q-icon name="place" color="grey" />
                  </template>
                </q-input>
          
          <q-input
                  ref="password"
                  :type="isPwd ? 'password' : 'text'"
                  v-model="user.password"
                  dense
                  label="Create password*"
                  lazy-rules
                  :rules="[
                    val => val !== null && val !== '' || 'Please enter your password',
                    val => val.length > 5 && val.length < 15 || 'Password must be 5 to 15 characters long.'
                  ]"
                >
                    <template v-slot:prepend>
                       <q-icon name="lock" color="grey" />
                    </template>
                    <template v-slot:append>
                    <q-icon
                        :name="isPwd ? 'visibility_off' : 'visibility'"
                        class="cursor-pointer"
                        @click="isPwd = !isPwd"
                    />
                    </template>
          </q-input>
                    <q-input
                  ref="password"
                  :type="isPwd ? 'password' : 'text'"
                  v-model="confirmpassword"
                  dense
                  label="Confirm password"
                  lazy-rules
                  :rules="[
                    val => val === user.password || 'Password does not match',
                
                  ]"
                >
                    <template v-slot:prepend>
                       <q-icon name="lock" color="grey" />
                    </template>
                    <template v-slot:append>
                    <q-icon
                        :name="isPwd ? 'visibility_off' : 'visibility'"
                        class="cursor-pointer"
                        @click="isPwd = !isPwd"
                    />
                    </template>
                </q-input> 
          <div v-if="this.user.click==false"> 
             <q-btn class="full-width" label="Submit" type="submit" color="primary"/>
          </div>
          <div v-else>
            <q-spinner-facebook
              color="primary"
              size="2em"
            />
          </div>

        </q-form>
        <div class="q-mt-sm q-mb-sm float-left my-font">
          Already have an Account? <router-link to='/' class="text-weight-medium text-primary" style="text-decoration:none">Login</router-link>
        </div>
      </div>
  </q-page>
</template> 

<script>
import axios from 'axios'
import  { mapActions } from 'vuex'
export default {
  data(){
    return{
    user:{
      name:null,
      phone:null,
      password:null,
      city:null,
      pincode:null,
      click:false
    },
     isPwd:false,
     options:['Indore','Bhopal'],
     confirmpassword:null,
    }
  },
  methods:{
      ...mapActions('store',['registerUser']),
    onSubmit(){
      this.user.click=true
     this.registerUser(this.user)
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