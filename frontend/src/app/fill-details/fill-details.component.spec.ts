import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FillDetailsComponent } from './fill-details.component';

describe('FillDetailsComponent', () => {
  let component: FillDetailsComponent;
  let fixture: ComponentFixture<FillDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FillDetailsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FillDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
