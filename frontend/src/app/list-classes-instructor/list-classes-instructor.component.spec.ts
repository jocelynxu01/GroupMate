import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListClassesInstructorComponent } from './list-classes-instructor.component';

describe('ListClassesInstructorComponent', () => {
  let component: ListClassesInstructorComponent;
  let fixture: ComponentFixture<ListClassesInstructorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListClassesInstructorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListClassesInstructorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
