import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DiplomaContainerComponent } from './diploma-container.component';

describe('DiplomaContainerComponent', () => {
  let component: DiplomaContainerComponent;
  let fixture: ComponentFixture<DiplomaContainerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DiplomaContainerComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DiplomaContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
