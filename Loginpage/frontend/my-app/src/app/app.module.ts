import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms'

import { AppComponent } from './app.component';
import { ShowDataComponent } from './show-data/show-data.component';
import { PagenotfoundComponent } from './pagenotfound/pagenotfound.component';

import { AppRoutingModule } from "./app.router";
import { UserLoginComponent } from './user-login/user-login.component';
import { HomeComponent } from './home/home.component';
import { RouterModule } from '@angular/router';
//import { RouterModule, Routes} from "@angular/router";

@NgModule({
  declarations: [
    AppComponent,
    ShowDataComponent,
    PagenotfoundComponent,
    UserLoginComponent,
    HomeComponent
  ],
  imports: [
    HttpModule,
    AppRoutingModule,
    BrowserModule,
    FormsModule,
    RouterModule.forRoot([{
      path:'home', component: HomeComponent
    }])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
