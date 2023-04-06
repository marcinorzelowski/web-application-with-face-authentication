import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {AuthService} from "../../../shared/services/auth.service";
import {ActivatedRoute, Router} from "@angular/router";
import {first} from "rxjs";
import {MatDialog} from "@angular/material/dialog";
import {CameraComponent} from "../../../shared/components/camera/camera.component";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  public form!: FormGroup;

  constructor(private authService: AuthService,
              private router: Router,
              public dialog: MatDialog) { }

  ngOnInit(): void {
    this.createForm();
  }

  private createForm(): void {
    this.form = new FormGroup({
      email: new FormControl("", [Validators.required]),
      password: new FormControl("", [Validators.required])
    })
  }

  onSubmit() {
    this.dialog.open(CameraComponent).afterClosed().subscribe(result => {
      this.authService.login(this.form.value, result).pipe(first()).subscribe({
        next: () => {
          this.router.navigate(['../diploma']);
        }
      })
    })

  }

  redirectToRegister() {
    this.router.navigate(['../auth/register']);

  }
}
