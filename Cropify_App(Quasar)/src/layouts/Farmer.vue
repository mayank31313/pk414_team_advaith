<template>
  <q-layout view="lHh Lpr lFf">
    <q-header
    v-if="!$route.path.includes('/chat')"
     elevated >
      <q-toolbar v-if="this.token!=null">
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />
          <q-img class="absolute-center"  height="50px" width="220px" src="statics/Cropify3.png" />
      </q-toolbar>
    </q-header>
    <q-header v-else>
      <q-btn
      flat
      color="black"
      icon="arrow_back"
      v-go-back.single
      
      />
    </q-header>
    <q-drawer
        v-model="leftDrawerOpen"
        show-if-above
        bordered
      >
          <q-scroll-area style="height: calc(100% - 150px); margin-top: 150px; border-right: 1px solid #ddd">
          <q-list padding class="q-gutter-sm">
             <q-item clickable  v-ripple:primary to="/home">
              <q-item-section avatar>
                <q-avatar square size="sm"><q-img src="statics/info.png"/></q-avatar>
              </q-item-section>

              <q-item-section>
                Latest News
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple:primary
            to="/crop"
            >
              <q-item-section avatar>
                <q-avatar square  size="sm"><q-img no-default-spinner src="statics/crops.png"/></q-avatar>
              </q-item-section>

              <q-item-section>
                Crop's Recommendations
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple:primary>
              <q-item-section avatar>
                <q-avatar square size="sm"><q-img src="statics/rupee.png"/></q-avatar>
              </q-item-section>

              <q-item-section>
                Get Crop's Price
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple:primary to="/chat/3">
              <q-item-section avatar>
                <q-avatar square size="sm"><q-img src="statics/article.png"/></q-avatar>
              </q-item-section>

              <q-item-section>
                GOVT. Advisories
              </q-item-section>
            </q-item>
            <q-item clickable v-ripple:primary>
              <q-item-section avatar>
                <q-avatar square size="sm"><q-img src="statics/question.png"/></q-avatar>
              </q-item-section>

              <q-item-section>
                Help
              </q-item-section>
            </q-item>
            <q-item clickable v-ripple:primary @click="logout">
              <q-item-section avatar>
                <q-avatar square size="sm"><q-img src="statics/logout.png"/></q-avatar>
              </q-item-section>

              <q-item-section>
                Logout
              </q-item-section>
            </q-item>
          </q-list>
          </q-scroll-area>
        <q-img no-default-spinner class="absolute-top bg-primary" src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQX1r4uELFlW5h-8qaJM52gPvbzw9czupU6eg&usqp=CAU"  style="height: 150px">
          <div class="absolute-bottom bg-transparent">
            <q-avatar size="56px" class="q-mb-sm bg-white">
              <q-img no-default-spinner src="https://image.flaticon.com/icons/svg/3174/3174924.svg"/>
            </q-avatar>
            <div class="text-weight-bold" v-if="userDetails.userDetails">{{ userDetails.userDetails.name }}</div>
            <div v-if="userDetails.userDetails">{{ userDetails.userDetails.username }}</div>
            <!-- <div @click="alt" v-ripple class="float-right" style="font-size:18px">
              Edit <q-icon size="xs" name="ti-pencil"/> -->
            </div>
          <!-- </div> -->
        </q-img>

      </q-drawer>


    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import  { mapActions, mapState } from 'vuex'
export default {
  name: 'MainLayout',
  data () {
    return {
      token : window.localStorage.getItem('token'),
      leftDrawerOpen: false,
      name:null,
      username:null
    }
  },
  computed:{
    ...mapState('store',['userDetails'])
  },
  methods:{
    ...mapActions('store', ['logoutUser']),
    alt(){
      alert('Clicked')
    },
    logout(){
      this.logoutUser()
    }
  }
}
</script>
