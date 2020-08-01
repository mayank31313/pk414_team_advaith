
const routes = [
  {
    path: '/',
    component: () => import('layouts/Farmer.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/register', component: () => import('pages/register.vue') },
      { path: '/home', component: () => import('pages/home.vue') },
      { path: '/crop', component: () => import('pages/Crops_recommendation.vue') },
      { path: '/output', component: () => import('pages/recommendedCrop.vue') },
      { path: '/price', component: () => import('pages/price.vue') },
      { path: '/chat/:id', component: () => import('pages/chat.vue') },
    ]
  },
  {
    path: '/admin',
    component: () => import('layouts/goverment.vue'),
    children: [
      { path: '', component: () => import('pages/queries.vue') },
      { path: '/production', component: () => import('pages/production.vue') },
      
    ]
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
