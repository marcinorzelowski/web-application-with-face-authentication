import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {TopMenuComponent} from "./components/top-menu/top-menu.component";
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatButtonModule} from "@angular/material/button";
import { CameraComponent } from './components/camera/camera.component';
import {WebcamModule} from "ngx-webcam";
import {MatDialogModule} from "@angular/material/dialog";
import { SafeUrlPipe } from './pipe/safe-url.pipe';



@NgModule({
  declarations: [
    TopMenuComponent,
    CameraComponent,
    SafeUrlPipe
  ],
  exports: [
    TopMenuComponent,
    SafeUrlPipe
  ],
  imports: [
    CommonModule,
    WebcamModule,
    MatToolbarModule,
    MatButtonModule,
    MatDialogModule
  ]
})
export class SharedModule { }
