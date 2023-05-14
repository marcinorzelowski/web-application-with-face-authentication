import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {AuthService} from "../../../shared/services/auth.service";
import {Router} from "@angular/router";
import {first} from "rxjs";
import {MatDialog} from "@angular/material/dialog";
import {CameraComponent} from "../../../shared/components/camera/camera.component";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  public form!: FormGroup;
  public files: File[] = [];

  constructor(private authService: AuthService,
              private router: Router,
              public dialog: MatDialog) { }

  ngOnInit(): void {
    this.createForm();
  }

  private createForm(): void {
    this.form = new FormGroup({
      firstName: new FormControl("", [Validators.required]),
      lastName: new FormControl("", [Validators.required]),
      email: new FormControl("", [Validators.required]),
      password: new FormControl("", [Validators.required])
    })
  }

  onSubmit() {
    this.authService.register(this.form.value, this.files).pipe(first()).subscribe({
      next: () => {
        this.router.navigate(['../diploma']);
      }
    })
  }

  public addImages(event: any): void {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      this.files = Array.from(target.files);
    } else {
      this.files = [];
    }
  }

  deleteImage(index: number): void {
    this.files.splice(index, 1);
  }

  redirectToLogin() {
    this.router.navigate(['../auth/login']);

  }

  public createImage(): void {
    this.dialog.open(CameraComponent).afterClosed().subscribe(result => {
      if (result instanceof File) {
        this.files.push(result);
      }
    })
  }
}
