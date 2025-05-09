import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewClassMembersComponent } from './view-class-members.component';

describe('ViewClassMembersComponent', () => {
  let component: ViewClassMembersComponent;
  let fixture: ComponentFixture<ViewClassMembersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewClassMembersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewClassMembersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
