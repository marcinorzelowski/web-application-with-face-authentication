import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DiplomantInfoComponent } from './diplomant-info.component';

describe('DiplomantInfoComponent', () => {
  let component: DiplomantInfoComponent;
  let fixture: ComponentFixture<DiplomantInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DiplomantInfoComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DiplomantInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
