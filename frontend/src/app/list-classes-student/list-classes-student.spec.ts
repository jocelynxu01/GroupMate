import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListClassesStudentComponent } from './list-classes-student.component';

describe('ListClassesInstructorComponent', () => {
  let component: ListClassesStudentComponent;
  let fixture: ComponentFixture<ListClassesStudentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListClassesStudentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListClassesStudentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
