<template>
  <q-page class="animate__animated animate__slideInUp" >
      <div class="q-pa-md text-center" >
        <label class="text-h4 text-primary my-font">
          Login
        </label>
        <q-form
          @submit.prevent.stop="onSubmit"
          class="q-gutter-md q-pa-xs q-mt-sm " 
        >
          <q-input
            dense
            type="tel"
            v-model="user.phone"
            hint="Phone Number*"
            label="Your phone*"
            lazy-rules
            maxlength="10"
            :rules="[
              val => val !== null  || 'Please type your phone no.',
              val => val.length===10 || 'Please type a valid phone.'
            ]"
          > 
             <template v-slot:prepend>
                      <q-icon name="phone" />
                    </template>
          </q-input>
          
          <q-input
                  square
                  dense
                  ref="password"
                  :type="isPwd ? 'password' : 'text'"
                  v-model="user.password"
                  hint="Password*"
                  label="Create password"
                  lazy-rules
                  :rules="[
                    val => val !== null && val !== '' || 'Please enter your password',
                    val => val.length > 5 && val.length < 15 || 'Password must be 5 to 15 characters long.'
                  ]"
                >
                    <template v-slot:prepend>
                      <q-icon name="lock" />
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
          Don't have an account ? <router-link to="/register" class="text-weight-medium text-primary" style="text-decoration:none">Create</router-link>
        </div>
      </div>
  </q-page>
</template> 

<script>
import { mapActions } from 'vuex'
export default {
  data(){
    return{
      user:{
        phone:null,
        password:null,
        click:false
      },
      isPwd:true,
    }
  },
  methods:{
    ...mapActions('store',['loginUser']),
    onSubmit(){
      this.user.click=true
     this.loginUser(this.user)
    }
  }
}
</script>
<style>
@import url('https://fonts.googleapis.com/css?family=Amarante');
@import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.0.0/animate.min.css');
.animate__animated.animate__slideInRIght {
  --animate-duration: 1s;
}
</style>