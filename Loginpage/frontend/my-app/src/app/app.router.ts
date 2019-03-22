import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ShowDataComponent } from './show-data/show-data.component';
import { PagenotfoundComponent } from './pagenotfound/pagenotfound.component';
import { UserLoginComponent} from './user-login/user-login.component'
import { HomeComponent } from './home/home.component';

const appRoutes: Routes = [
    // {
    //     path:"",
    //     component: ShowDataComponent,
    // },
    // {
    //     path:"**",
    //     component: PagenotfoundComponent,
    // }
    {
        path:"userLogin",
        component: UserLoginComponent,
    },
    
    { path:"home",
      component:HomeComponent,

    }
]

@NgModule({
    imports: [
        RouterModule.forRoot(
            appRoutes
        )
    ],
    exports: [
        RouterModule
    ]
})

export class AppRoutingModule{}