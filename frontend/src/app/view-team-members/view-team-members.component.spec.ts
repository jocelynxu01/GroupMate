import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewTeamMembersComponent } from './view-team-members.component';

describe('ViewTeamMembersComponent', () => {
  let component: ViewTeamMembersComponent;
  let fixture: ComponentFixture<ViewTeamMembersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewTeamMembersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewTeamMembersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
