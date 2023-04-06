import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";

@Component({
  selector: 'app-auth-card',
  templateUrl: './auth-card.component.html',
  styleUrls: ['./auth-card.component.css']
})
export class AuthCardComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  getTitle() {
    if (this.router.url === '/auth/login') {
      return 'Sign in';
    } else {
      return 'Sign up';
    }
  }
}
