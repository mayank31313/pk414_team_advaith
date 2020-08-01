<template>
  <q-layout view="lHh Lpr lFf">
    <!-- Mobile layout -->
    <div class="layout">
      <q-header
       v-if="!$route.path.includes('/chat')"
      elevated >
      <q-toolbar>
        <q-img no-default-spinner class="absolute-center"  height="50px" width="220px" src="statics/Cropify3.png" />
        <div class="absolute-right row justify-center">
            <q-btn
            flat
            v-if="username"
            class="col"
            size="md"
            icon="notifications"
            />
            <q-btn
            class="col"
            size="sm"
            flat
            @click="logout"
            no-caps
            :label="username ? 'Logout' : 'Login'"
            />
        </div>
      </q-toolbar>
    </q-header>
      <q-footer reveal elevated>
        <q-toolbar class="bg-white text-black shadow-2">
          <div class="tabs">
            <q-tabs v-model="tab1" active-color="primary">  
              <q-tab name="tab1" style="width:25%">
                <router-link to="" style="text-decoration:none">
                <q-avatar size="md">
              <q-img no-default-spinner src="https://image.flaticon.com/icons/svg/3248/3248144.svg"/>
            </q-avatar><br/>
            <label  class="text-center tab-text" >Queries?</label>
                </router-link>
              </q-tab>
                <q-separator vertical inset />
              <q-tab name="tab2" style="width:25%">
                <router-link to="" style="text-decoration:none">
                <q-avatar square size="sm"><q-img no-default-spinner src="https://image.flaticon.com/icons/svg/3029/3029337.svg"/></q-avatar><br>
                <label  class="text-center tab-text" >Production Report</label>
                </router-link>
              </q-tab>
                <!-- <q-separator vertical inset /> -->
                <q-separator vertical inset />
              <q-tab name="tab4" style="width:25%;">
                <router-link to="" style="text-decoration:none">
                <q-avatar size="md">
              <q-img no-default-spinner src="https://image.flaticon.com/icons/svg/3174/3174924.svg"/>
            </q-avatar><br/>
            <label class="text-center tab-text text-caption" >Farmer Details</label>
                </router-link>
              </q-tab>
            </q-tabs>
          </div>
        </q-toolbar>
      </q-footer>
    <q-page-container class="full-height">
      <router-view/>
    </q-page-container>        


    </div>
  </q-layout>

</template>

<script>
import { mapActions } from 'vuex'

export default {
  data () {
    return {
      tab1:'tab1',
      username:window.localStorage.getItem('username'),
      }
  },
  methods:{
    ...mapActions('store', ['logoutUser']),
    logout(){
      this.logoutUser()
    }
  }
}
</script>
<style>
.layout{
  max-width: 600px;
}
.tabs{
  width: 100%;
}
.tab-text{
  font-family: Arial, Helvetica, sans-serif;
  font-weight: bolder;
  font-size: 8px;
  color:grey;
}
</style> 
